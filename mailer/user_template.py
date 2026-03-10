from datetime import datetime
from utils.helpers import https, label


def build(name: str, website_key: str) -> str:
    url  = https(website_key)
    lbl  = label(website_key)
    year = datetime.now().year

    return f"""
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
  "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Thank You for Contacting Us</title>
  <!--[if mso]>
  <style>body, table, td {{font-family: Arial, Helvetica, sans-serif !important;}}</style>
  <![endif]-->
</head>
<body style="margin:0;padding:0;background-color:#fef3f2;">

  <!-- Hidden preview text -->
  <div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">
    Thank you for reaching out! We'll respond within 24 hours.
  </div>

  <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
         style="background-color:#fef3f2;">
    <tr><td align="center" style="padding:30px 15px;">

      <table role="presentation" width="600" cellpadding="0" cellspacing="0"
             style="max-width:600px;width:100%;">

        <!-- Card -->
        <tr><td>
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
                 style="background-color:#ffffff;border-radius:8px;overflow:hidden;
                        box-shadow:0 4px 6px rgba(0,0,0,0.07);">

            <!-- Top accent -->
            <tr><td style="height:5px;background-color:#f97316;"></td></tr>

            <!-- Heading -->
            <tr><td align="center" style="padding:40px 40px 10px;">
              <h1 style="margin:0;font-family:Arial,sans-serif;font-size:26px;
                          font-weight:bold;color:#1f2937;">Message Received!</h1>
            </td></tr>

            <!-- Sub-heading -->
            <tr><td align="center" style="padding:0 40px 30px;">
              <p style="margin:0;font-family:Arial,sans-serif;font-size:16px;color:#6b7280;">
                Thank you for getting in touch with us
              </p>
            </td></tr>

            <!-- Divider -->
            <tr><td style="padding:0 40px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                <tr><td style="height:1px;background-color:#e5e7eb;"></td></tr>
              </table>
            </td></tr>

            <!-- Greeting -->
            <tr><td style="padding:30px 40px 20px;">
              <p style="margin:0;font-family:Arial,sans-serif;font-size:16px;color:#374151;">
                Hello <strong style="color:#1f2937;">{name}</strong>,
              </p>
            </td></tr>

            <!-- Body -->
            <tr><td style="padding:0 40px 20px;">
              <p style="margin:0;font-family:Arial,sans-serif;font-size:15px;
                        color:#4b5563;line-height:1.8;">
                We've successfully received your message and it has been forwarded
                to our support team for review.
              </p>
            </td></tr>

            <!-- Info box -->
            <tr><td style="padding:0 40px 25px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
                     style="background-color:#fff7ed;border-left:4px solid #f97316;
                            border-radius:0 6px 6px 0;">
                <tr><td style="padding:20px;">
                  <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                    <tr>
                      <td width="50" valign="top"><span style="font-size:24px;">⏱️</span></td>
                      <td valign="top">
                        <p style="margin:0 0 5px;font-family:Arial,sans-serif;font-size:14px;
                                  font-weight:bold;color:#1f2937;">Expected Response Time</p>
                        <p style="margin:0;font-family:Arial,sans-serif;font-size:14px;
                                  color:#6b7280;line-height:1.6;">
                          Our team typically responds within
                          <strong style="color:#f97316;">24 hours</strong> on business days.
                        </p>
                      </td>
                    </tr>
                  </table>
                </td></tr>
              </table>
            </td></tr>

            <!-- Extra note -->
            <tr><td style="padding:0 40px 30px;">
              <p style="margin:0;font-family:Arial,sans-serif;font-size:15px;
                        color:#4b5563;line-height:1.8;">
                If your request requires additional information, a team member will
                contact you directly using the email address you provided.
              </p>
            </td></tr>

            <!-- CTA -->
            <tr><td align="center" style="padding:10px 40px 40px;">
              <table role="presentation" cellpadding="0" cellspacing="0">
                <tr><td align="center"
                        style="border-radius:6px;background-color:#f97316;">
                  <a href="{url}" target="_blank"
                     style="display:inline-block;padding:16px 36px;
                            font-family:Arial,sans-serif;font-size:16px;
                            font-weight:bold;color:#ffffff;text-decoration:none;
                            border-radius:6px;">
                    Visit Our Website →
                  </a>
                </td></tr>
              </table>
            </td></tr>

          </table>
        </td></tr>

        <!-- "While you wait" block -->
        <tr><td style="padding:25px 0;">
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
                 style="background-color:#ffffff;border-radius:8px;">
            <tr><td style="padding:25px 30px;">
              <p style="margin:0 0 15px;font-family:Arial,sans-serif;font-size:14px;
                        font-weight:bold;color:#1f2937;">💡 While you wait, you can:</p>
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                <tr><td style="padding:8px 0;">
                  <span style="font-family:Arial,sans-serif;font-size:14px;color:#4b5563;">
                    ✦ &nbsp; Explore our services and offerings
                  </span>
                </td></tr>
                <tr><td style="padding:8px 0;">
                  <span style="font-family:Arial,sans-serif;font-size:14px;color:#4b5563;">
                    ✦ &nbsp; Check out our latest updates
                  </span>
                </td></tr>
                <tr><td style="padding:8px 0;">
                  <span style="font-family:Arial,sans-serif;font-size:14px;color:#4b5563;">
                    ✦ &nbsp; Browse our FAQ section
                  </span>
                </td></tr>
              </table>
            </td></tr>
          </table>
        </td></tr>

        <!-- Footer -->
        <tr><td style="padding:20px 0;">
          <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
            <tr><td align="center" style="padding:0 20px 20px;">
              <p style="margin:0;font-family:Arial,sans-serif;font-size:13px;color:#9ca3af;">
                If you did not submit this request, you may safely ignore this email.
              </p>
            </td></tr>
            <tr><td style="padding:0 40px 20px;">
              <table role="presentation" width="100%" cellpadding="0" cellspacing="0">
                <tr><td style="height:1px;background-color:#e5e7eb;"></td></tr>
              </table>
            </td></tr>
            <tr><td align="center" style="padding:0 20px 10px;">
              <p style="margin:0;font-family:Arial,sans-serif;font-size:14px;
                        font-weight:bold;color:#6b7280;">{lbl}</p>
            </td></tr>
            <tr><td align="center" style="padding:10px 20px;">
              <p style="margin:0;font-family:Arial,sans-serif;font-size:12px;color:#9ca3af;">
                © {year} {lbl}. All rights reserved.
              </p>
            </td></tr>
            <tr><td align="center" style="padding:15px 20px 0;">
              <p style="margin:0;font-family:Arial,sans-serif;font-size:11px;color:#d1d5db;">
                This is an automated confirmation email. Please do not reply directly.
              </p>
            </td></tr>
          </table>
        </td></tr>

      </table>
    </td></tr>
  </table>
</body>
</html>
"""
