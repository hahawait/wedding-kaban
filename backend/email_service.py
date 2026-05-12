import os
import httpx

RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
FROM_EMAIL = os.getenv("FROM_EMAIL", "onboarding@resend.dev")
COUPLE_EMAIL = os.getenv("COUPLE_EMAIL", "")
REPLY_TO = os.getenv("REPLY_TO", "").strip()


def _email_to_ascii(addr: str) -> str:
    """Resend принимает from/to в ASCII; кириллический домен (.рф) → punycode (xn--...)."""
    addr = addr.strip()
    if "@" not in addr:
        return addr
    local, domain = addr.rsplit("@", 1)
    if not domain or all(ord(c) < 128 for c in domain):
        return addr
    try:
        ascii_domain = ".".join(
            label.encode("idna").decode("ascii") for label in domain.split(".") if label
        )
    except (UnicodeError, UnicodeDecodeError):
        return addr
    return f"{local}@{ascii_domain}"


def _build_html(guest_name: str) -> str:
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="background-color:#FFF0F5;margin:0;padding:0;font-family:Times New Roman,serif;">

<table width="600" border="0" cellpadding="0" cellspacing="0" align="center"
       style="background-color:#FFFFFF;border:3px solid #CC0000;margin:20px auto;">

  <!-- Шапка -->
  <tr>
    <td align="center" style="background-color:#CC0000;padding:16px;">
      <span style="font-family:Arial,sans-serif;font-size:22px;font-weight:bold;color:#FFFF00;">
        ✦ СВАДЬБА КИРИЛЛА И ЛЕНЫ ✦
      </span><br>
      <span style="font-family:Times New Roman,serif;font-size:15px;color:#FFFFFF;">
        Сентябрь 2026 года
      </span>
    </td>
  </tr>

  <!-- Розовая полоска -->
  <tr>
    <td style="background-color:#FFB6C1;padding:6px;text-align:center;">
      <span style="font-family:Arial,sans-serif;font-size:13px;color:#8B0000;font-weight:bold;">
        ♥ &nbsp; СОВЕТ ДА ЛЮБОВЬ!! &nbsp; ♥ &nbsp; ГОРЬКО!! &nbsp; ♥
      </span>
    </td>
  </tr>

  <!-- Основной текст -->
  <tr>
    <td style="padding:24px 30px;">
      <p style="font-family:Arial,sans-serif;font-size:16px;color:#CC0000;font-weight:bold;margin:0 0 12px;">
        Дорогой(ая) {guest_name}!!
      </p>
      <p style="font-family:Times New Roman,serif;font-size:14px;color:#000000;line-height:1.7;margin:0 0 12px;">
        Мы очень рады, что вы решили разделить с нами этот особенный день!!
        Ваша регистрация прошла успешно, и мы с нетерпением ждём вас на нашей свадьбе!
      </p>
      <p style="font-family:Times New Roman,serif;font-size:14px;color:#000000;line-height:1.7;margin:0 0 12px;">
        Точную дату, место и время мы сообщим вам дополнительно — следите за новостями
        на нашем сайте!! Пожалуйста не забудьте подтвердить своё присутствие до
        <strong>1 августа 2026 года</strong>.
      </p>
      <p style="font-family:Times New Roman,serif;font-size:13px;color:#FF1493;font-style:italic;margin:0 0 16px;">
        «Любовь — это не то что ты находишь. Любовь — это то что находит тебя.»
      </p>

      <!-- Блок деталей -->
      <table width="100%" border="1" cellpadding="8" cellspacing="0"
             style="border-color:#FF69B4;margin-bottom:16px;">
        <tr style="background-color:#FFB6C1;">
          <td colspan="2" align="center"
              style="font-family:Arial,sans-serif;font-size:13px;font-weight:bold;color:#8B0000;">
            ДЕТАЛИ ТОРЖЕСТВА
          </td>
        </tr>
        <tr style="background-color:#FFF0F5;">
          <td style="font-family:Arial,sans-serif;font-size:13px;font-weight:bold;width:120px;">
            📅 Дата:
          </td>
          <td style="font-family:Times New Roman,serif;font-size:14px;">
            <strong>Сентябрь 2026 года</strong><br>
            <span style="color:#888888;font-size:12px;">(точная дата уточняется)</span>
          </td>
        </tr>
        <tr>
          <td style="font-family:Arial,sans-serif;font-size:13px;font-weight:bold;">
            📍 Место:
          </td>
          <td style="font-family:Times New Roman,serif;font-size:14px;">
            Уточняется — сообщим дополнительно
          </td>
        </tr>
      </table>

      <p style="font-family:Arial,sans-serif;font-size:14px;color:#CC0000;font-weight:bold;
                text-align:center;margin:0;">
        С ЛЮБОВЬЮ — КИРИЛЛ &amp; ЛЕНА ❤
      </p>
    </td>
  </tr>

  <!-- Подвал -->
  <tr>
    <td align="center" style="background-color:#8B0000;padding:10px;">
      <span style="font-family:Arial,sans-serif;font-size:11px;color:#FFCCCC;">
        По вопросам: kirill_lena_2026@mail.ru &nbsp;|&nbsp; Создано с любовью ❤
      </span>
    </td>
  </tr>

</table>
</body>
</html>"""


def send_invitation(guest_name: str, guest_email: str) -> None:
    if not RESEND_API_KEY:
        print(f"[EMAIL SKIP] RESEND_API_KEY не задан. Письмо для {guest_email} не отправлено.")
        return

    from_addr = _email_to_ascii(FROM_EMAIL)
    to_guest = _email_to_ascii(guest_email.strip())
    recipients = [to_guest]
    if COUPLE_EMAIL and COUPLE_EMAIL.strip():
        recipients.append(_email_to_ascii(COUPLE_EMAIL.strip()))

    payload = {
        "from": from_addr,
        "to": recipients,
        "subject": "✦ Кирилл и Лена приглашают вас на свадьбу! ❤",
        "html": _build_html(guest_name),
    }
    if REPLY_TO:
        payload["reply_to"] = _email_to_ascii(REPLY_TO)

    response = httpx.post(
        "https://api.resend.com/emails",
        headers={
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json",
        },
        json=payload,
        timeout=10,
    )
    if not response.is_success:
        print(f"[EMAIL ERROR] {response.status_code} {response.text}")
    response.raise_for_status()
    try:
        rid = response.json().get("id")
    except Exception:
        rid = None
    print(
        f"[EMAIL OK] to={guest_email} http={response.status_code}"
        + (f" resend_id={rid}" if rid else "")
        + " — если в Gmail пусто: Resend → Emails → это письмо (Delivered/Bounced) и поиск in:anywhere по теме"
    )
