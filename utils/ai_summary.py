import os
import re

import streamlit as st
from dotenv import load_dotenv

# The AI summary is an optional enhancement.  Keeping this import optional
# lets the core disease-assessment app start even if the OpenAI SDK has not
# been installed in the active Python environment yet.
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

load_dotenv()

client = (
    OpenAI(
        api_key=os.getenv("OPENROUTER_API_KEY"),
        base_url="https://openrouter.ai/api/v1"
    )
    if OpenAI and os.getenv("OPENROUTER_API_KEY")
    else None
)

MODEL_NAME = "nvidia/nemotron-nano-9b-v2:free"

# Small, CPU-friendly local model used only as a fallback if
# OpenRouter is unreachable (no key, network issue, rate limit, etc.)
# — English generation only. Small local models tend to write weak,
# unnatural Arabic, so Arabic is handled separately via real
# translation (see _translate_to_arabic below), never generated
# directly by the LLM.
LOCAL_MODEL_NAME = "Qwen/Qwen2.5-0.5B-Instruct"


# ==================================================
# SECTION 1: Prompt building (English generation only)
# ==================================================

def _build_prompt(disease, patient_data, probability, risk_level):

    return f"""
You are a medical assistant explaining a risk-screening result to a patient
in person — warm, clear, and organized, like a doctor who takes time to
explain things properly.

Write your entire response in English.

Disease:
{disease}

Risk Level:
{risk_level}

Risk Probability:
{probability:.0%}

Patient Data:
{patient_data}

Structure your response into exactly four clearly separated paragraphs,
each starting with a short plain-text label followed by a colon, like this:

Result:
(2-3 sentences explaining what this result means in plain terms.)

Contributing Factors:
(3-5 sentences discussing which specific data points from the patient's
information may have influenced this result, referencing the actual values
where relevant.)

Recommendations:
(4-6 concrete, actionable suggestions the patient can follow, each as its
own short sentence starting with "• " — for example diet, activity, sleep,
follow-up checkups, or monitoring specific values. Be specific to this
patient's data, not generic.)

Next Steps:
(1-2 sentences on what the patient should do next, e.g. when to see a
doctor.)

Formatting requirements — follow these exactly:
- Each of the four labels (Result:, Contributing Factors:, Recommendations:,
  Next Steps:) must appear alone on its own line, with nothing else on
  that line.
- Do NOT use any Markdown formatting at all: no asterisks, no double
  asterisks, no hashtags, no backticks, no numbered lists with periods.
- The only bullet character allowed is "• " at the start of each
  recommendation line, nothing else.
- Do not diagnose. Do not mention AI or machine learning.
- Be supportive, clear, and specific — avoid vague filler sentences.
- Total length: 250-400 words. Always finish every section completely.
""".strip()


# ==================================================
# SECTION 2: Primary — OpenRouter
# ==================================================

def _call_openrouter(prompt):
    if client is None:
        return None

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            max_tokens=1300,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        content = response.choices[0].message.content
        return content.strip() if content else None

    except Exception:
        return None


# ==================================================
# SECTION 3: Fallback — small local model (English only)
# ==================================================

@st.cache_resource(show_spinner="Loading local backup model (first time only)...")
def _load_local_model():
    from transformers import AutoModelForCausalLM, AutoTokenizer

    tokenizer = AutoTokenizer.from_pretrained(LOCAL_MODEL_NAME)
    model = AutoModelForCausalLM.from_pretrained(LOCAL_MODEL_NAME)

    return tokenizer, model


def _call_local_model(prompt):
    try:
        tokenizer, model = _load_local_model()

        messages = [{"role": "user", "content": prompt}]

        prompt_text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )

        inputs = tokenizer(prompt_text, return_tensors="pt")

        output_ids = model.generate(
            **inputs,
            max_new_tokens=400,
            do_sample=False
        )

        new_tokens = output_ids[0][inputs["input_ids"].shape[-1]:]
        response = tokenizer.decode(new_tokens, skip_special_tokens=True).strip()

        return response if response else None

    except Exception:
        return None


# ==================================================
# SECTION 4: English summary generation (main entry point)
# ==================================================

def generate_ai_summary(disease, patient_data, probability, risk_level):
    """
    Generate a simple, patient-facing explanation of the risk result,
    in English.

    Tries, in order:
      1. OpenRouter (cloud LLM) — best quality.
      2. A small local model (Qwen2.5-0.5B-Instruct) — runs fully
         offline, used only if OpenRouter fails for any reason.
      3. A static templated message — always succeeds.

    Arabic is never generated directly by an LLM here — see
    render_ai_summary_section, which translates this English text
    with Google Translate instead (small local models write weak,
    unnatural Arabic).
    """

    prompt = _build_prompt(disease, patient_data, probability, risk_level)

    content = _call_openrouter(prompt)
    if content:
        return _clean_markdown(content)

    content = _call_local_model(prompt)
    if content:
        return _clean_markdown(content)

    return _fallback_summary(disease, risk_level, probability)


def _clean_markdown(text):
    """
    Safety net in case the model still slips in Markdown syntax
    despite the prompt instructions. Strips bold/italic/heading/code
    markers and normalizes stray "-"/"*" bullets to the plain "•"
    character we actually want, without touching normal punctuation.
    """

    # Bold / italic markers
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"(?<!\w)\*(.*?)\*(?!\w)", r"\1", text)

    # Headings ("# ", "## ", ...)
    text = re.sub(r"^\s{0,3}#{1,6}\s*", "", text, flags=re.MULTILINE)

    # Inline / block code markers
    text = text.replace("```", "").replace("`", "")

    # Bullet dashes/asterisks at line start -> plain bullet
    text = re.sub(r"^\s*[-*]\s+", "• ", text, flags=re.MULTILINE)

    return text.strip()


def _fallback_summary(disease, risk_level, probability):
    return (
        f"Based on the information provided, your estimated {disease} risk level "
        f"is {risk_level} (around {probability:.0%}). We couldn't generate a "
        f"personalized explanation right now, but we'd recommend reviewing your "
        f"results above and discussing them with a healthcare professional if "
        f"you have any concerns."
    )


# ==================================================
# SECTION 5: Arabic — real translation, not LLM generation
# ==================================================

def _translate_to_arabic(text):
    """
    Translates the given English text to Arabic using Google
    Translate (via the deep-translator package). Returns None if
    translation fails for any reason (no internet, package missing,
    etc.) so the caller can fall back to a static Arabic message.
    """

    try:
        from deep_translator import GoogleTranslator

        return GoogleTranslator(source="en", target="ar").translate(text)

    except Exception:
        return None


def _fallback_summary_ar(disease, risk_level, probability):
    return (
        f"بناءً على البيانات اللي إدخلتها، مستوى الخطورة المتوقع لـ{disease} "
        f"هو {risk_level} (حوالي {probability:.0%}). للأسف مقدرناش نولّد شرح "
        f"مخصص دلوقتي، وننصحك تراجع النتيجة اللي فوق وتتكلم مع دكتور مختص "
        f"لو عندك أي قلق."
    )


# ==================================================
# SECTION 6: Streamlit UI — shared "AI Summary" section used by
# every disease page (heart, stroke, diabetes, kidney, breast...).
# ==================================================

def render_ai_summary_section(page_key, disease_label, patient_data, probability, risk_level):
    """
    Shared "AI Summary" block used by every disease page:

      - "Generate Health Summary" button (generates in English via
        the LLM).
      - The result shown in a styled card.
      - A "Translate to Arabic" button that translates the already
        -generated English text with Google Translate (fast, no LLM
        call, and much more natural Arabic than asking a small model
        to write it from scratch) — and a "View in English" button
        to switch back. Both versions are cached so switching between
        them doesn't repeat any work.
      - A "Download Report" button that bundles the patient's info +
        risk result + the currently displayed summary into one text
        file, in whichever language is currently shown.

    page_key: short unique prefix for this page's session_state /
              widget keys, e.g. "heart", "stroke", "kidney", "diabetes",
              "breast".
    """

    summary_en_key = f"{page_key}_ai_summary_en"
    summary_ar_key = f"{page_key}_ai_summary_ar"
    shown_lang_key = f"{page_key}_ai_summary_lang"

    st.subheader("🤖 AI Health Summary")

    if st.button(
        "🧠 Generate Health Summary",
        use_container_width=True,
        key=f"{page_key}_generate_summary"
    ):

        with st.spinner("Generating health summary..."):

            summary_text = generate_ai_summary(
                disease=disease_label,
                patient_data=patient_data,
                probability=probability,
                risk_level=risk_level
            )

        st.session_state[summary_en_key] = summary_text
        st.session_state.pop(summary_ar_key, None)
        st.session_state[shown_lang_key] = "en"

    if summary_en_key not in st.session_state:
        return

    shown_lang = st.session_state.get(shown_lang_key, "en")

    display_text = (
        st.session_state.get(summary_ar_key, "")
        if shown_lang == "ar"
        else st.session_state[summary_en_key]
    )

    _render_summary_card(display_text, shown_lang)

    st.write("")

    action_col, download_col = st.columns(2)

    with action_col:

        if shown_lang == "en":

            if st.button(
                "🌐 Translate to Arabic",
                use_container_width=True,
                key=f"{page_key}_translate_ar"
            ):

                if summary_ar_key not in st.session_state:

                    with st.spinner("جاري الترجمة..."):
                        translated = _translate_to_arabic(st.session_state[summary_en_key])

                        st.session_state[summary_ar_key] = (
                            translated
                            if translated
                            else _fallback_summary_ar(disease_label, risk_level, probability)
                        )

                st.session_state[shown_lang_key] = "ar"
                st.rerun()

        else:

            if st.button(
                "🌐 View in English",
                use_container_width=True,
                key=f"{page_key}_view_en"
            ):
                st.session_state[shown_lang_key] = "en"
                st.rerun()

    with download_col:

        report_text = _build_report_text(
            disease_label, patient_data, probability, risk_level,
            display_text, shown_lang
        )

        file_suffix = "ar" if shown_lang == "ar" else "en"

        st.download_button(
            label="⬇️ Download Report",
            data=report_text,
            file_name=f"{page_key}_report_{file_suffix}.txt",
            mime="text/plain",
            use_container_width=True,
            key=f"{page_key}_download_report"
        )


def _format_summary_html(text):
    """
    Turns the plain-text summary into structured HTML: short lines
    ending in ":" become section headers, and "• " lines become a
    real HTML bullet list. Works language-agnostically (English or
    the translated Arabic) since it detects labels by shape (short,
    ends with ":") rather than matching specific English words.
    """

    lines = [line.strip() for line in text.split("\n")]

    html_parts = []
    in_list = False

    def close_list():
        nonlocal in_list
        if in_list:
            html_parts.append("</ul>")
            in_list = False

    for line in lines:

        if not line:
            continue

        if line.startswith("• "):
            if not in_list:
                html_parts.append('<ul style="margin:4px 0 12px 0; padding-inline-start:22px;">')
                in_list = True
            html_parts.append(f'<li style="margin-bottom:6px;">{line[2:].strip()}</li>')
            continue

        is_label = line.endswith(":") and len(line.split()) <= 5

        close_list()

        if is_label:
            html_parts.append(
                f'<h4 style="color:#0077B6; margin:16px 0 6px 0; font-size:16px;">{line}</h4>'
            )
        else:
            html_parts.append(f'<p style="margin:4px 0;">{line}</p>')

    close_list()

    return "".join(html_parts)


def _render_summary_card(text, language):

    direction = "rtl" if language == "ar" else "ltr"
    text_align = "right" if language == "ar" else "left"

    formatted_html = _format_summary_html(text)

    card_html = (
        '<div style="'
        'background:#EAF7FF; border:1px solid #BDE3F7; '
        'border-radius:20px; padding:24px; margin-top:6px; '
        f'direction:{direction}; text-align:{text_align}; '
        'line-height:1.8; color:#1f2937; font-size:15.5px;">'
        f'{formatted_html}'
        '</div>'
    )

    st.markdown(card_html, unsafe_allow_html=True)


def _build_report_text(disease_label, patient_data, probability, risk_level, summary_text, language):

    if language == "ar":

        lines = [
            f"تقرير {disease_label}",
            "=" * 40,
            "",
            "البيانات الشخصية:",
        ]

        for key, value in patient_data.items():
            lines.append(f"- {key}: {value}")

        lines += [
            "",
            f"مستوى الخطورة: {risk_level}",
            f"نسبة الخطورة: {probability:.0%}",
            "",
            "ملخص الذكاء الاصطناعي:",
            "-" * 40,
            summary_text,
        ]

    else:

        lines = [
            f"{disease_label} Report",
            "=" * 40,
            "",
            "Patient Information:",
        ]

        for key, value in patient_data.items():
            lines.append(f"- {key}: {value}")

        lines += [
            "",
            f"Risk Level: {risk_level}",
            f"Risk Probability: {probability:.0%}",
            "",
            "AI Summary:",
            "-" * 40,
            summary_text,
        ]

    return "\n".join(lines)
