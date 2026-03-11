"""Admin email template for new lead notifications."""

from datetime import datetime
from utils.helpers import https, label, dash


def build(name: str, email: str, phone: str, message: str,
          website_key: str, product: str, product_type: str,
          ip_address: str) -> str:
    """Render the admin notification HTML email."""
    url  = https(website_key)
    lbl  = label(website_key)
    ts   = datetime.now().strftime("%B %d, %Y - %I:%M %p")
    year = datetime.now().year

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>New Lead</title>
</head>
<body style="margin:0;padding:0;background-color:#f0f4f8;
             font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Helvetica,Arial,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0" bgcolor="#f0f4f8"
       style="background-color:#f0f4f8;padding:40px 16px;">
<tr><td align="center">

  <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;width:100%;">

    
    <tr>
      <td align="center" style="padding-bottom:24px;">
        <span style="display:inline-block;background-color:#dde3ed;border-radius:100px;
                     padding:6px 20px;color:#64748b;font-size:12px;font-weight:600;
                     letter-spacing:2px;text-transform:uppercase;">
          {lbl} &nbsp;&nbsp; Admin Panel
        </span>
      </td>
    </tr>

    
    <tr>
      <td style="background-color:#ffffff;border-radius:16px;overflow:hidden;
                 border:1px solid #e2e8f0;">

        
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td style="height:4px;background-color:#6366f1;"></td>
            <td style="height:4px;background-color:#8b5cf6;"></td>
            <td style="height:4px;background-color:#ec4899;"></td>
          </tr>
        </table>

        
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td style="background-color:#1e1b4b;padding:36px 44px 30px;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="vertical-align:middle;">
                    <table cellpadding="0" cellspacing="0" style="margin-bottom:14px;">
                      <tr>
                        <td style="background-color:#312e81;border-radius:100px;padding:5px 14px;">
                          <span style="color:#a5b4fc;font-size:11px;font-weight:700;
                                       letter-spacing:1.5px;text-transform:uppercase;">
                             New Lead
                          </span>
                        </td>
                      </tr>
                    </table>
                    <h1 style="margin:0 0 8px;color:#ffffff;font-size:24px;font-weight:800;">
                      You have a new lead!
                    </h1>
                    <p style="margin:0;color:#818cf8;font-size:13px;">{ts}</p>
                  </td>
                  <td width="64" style="vertical-align:middle;text-align:right;">
                    <div style="width:58px;height:58px;background-color:#4f46e5;
                                border-radius:14px;text-align:center;line-height:58px;
                                font-size:24px;"></div>
                  </td>
                </tr>
              </table>

              
              <table width="100%" cellpadding="0" cellspacing="0" style="margin-top:20px;">
                <tr>
                  <td style="background-color:#312e81;border-radius:8px;padding:10px 16px;">
                    <table cellpadding="0" cellspacing="0"><tr>
                      <td style="color:#818cf8;font-size:11px;font-weight:600;
                                  letter-spacing:1px;text-transform:uppercase;
                                  padding-right:10px;">Source</td>
                      <td>
                        <a href="{url}" style="color:#c7d2fe;font-size:13px;
                                               font-weight:700;text-decoration:none;">
                           &nbsp;{lbl}
                        </a>
                      </td>
                    </tr></table>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>

        
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td style="background-color:#ffffff;padding:36px 44px 40px;">

              <p style="margin:0 0 16px;color:#94a3b8;font-size:11px;font-weight:700;
                        letter-spacing:2px;text-transform:uppercase;">Contact Details</p>

              <table width="100%" cellpadding="0" cellspacing="0"
                     style="border:1px solid #e2e8f0;border-radius:12px;
                            overflow:hidden;margin-bottom:28px;">

                
                <tr>
                  <td width="130" style="padding:14px 16px;background-color:#f8faff;
                                         border-right:1px solid #e2e8f0;
                                         border-bottom:1px solid #e2e8f0;vertical-align:middle;">
                    <span style="color:#94a3b8;font-size:11px;font-weight:700;
                                 letter-spacing:1px;text-transform:uppercase;">Name</span>
                  </td>
                  <td style="padding:14px 18px;border-bottom:1px solid #e2e8f0;
                             vertical-align:middle;background-color:#ffffff;">
                    <span style="color:#0f172a;font-size:15px;font-weight:700;">{name}</span>
                  </td>
                </tr>

                
                <tr>
                  <td style="padding:14px 16px;background-color:#f8faff;
                             border-right:1px solid #e2e8f0;
                             border-bottom:1px solid #e2e8f0;vertical-align:middle;">
                    <span style="color:#94a3b8;font-size:11px;font-weight:700;
                                 letter-spacing:1px;text-transform:uppercase;">Email</span>
                  </td>
                  <td style="padding:14px 18px;border-bottom:1px solid #e2e8f0;
                             vertical-align:middle;background-color:#ffffff;">
                    <a href="mailto:{email}"
                       style="color:#4f46e5;font-size:14px;font-weight:600;
                              text-decoration:none;">{email}</a>
                  </td>
                </tr>

                
                <tr>
                  <td style="padding:14px 16px;background-color:#f8faff;
                             border-right:1px solid #e2e8f0;
                             border-bottom:1px solid #e2e8f0;vertical-align:middle;">
                    <span style="color:#94a3b8;font-size:11px;font-weight:700;
                                 letter-spacing:1px;text-transform:uppercase;">Phone</span>
                  </td>
                  <td style="padding:14px 18px;border-bottom:1px solid #e2e8f0;
                             vertical-align:middle;background-color:#ffffff;">
                    <span style="color:#334155;font-size:14px;">{dash(phone)}</span>
                  </td>
                </tr>

                
                <tr>
                  <td style="padding:14px 16px;background-color:#f8faff;
                             border-right:1px solid #e2e8f0;
                             border-bottom:1px solid #e2e8f0;vertical-align:middle;">
                    <span style="color:#94a3b8;font-size:11px;font-weight:700;
                                 letter-spacing:1px;text-transform:uppercase;">Website</span>
                  </td>
                  <td style="padding:14px 18px;border-bottom:1px solid #e2e8f0;
                             vertical-align:middle;background-color:#ffffff;">
                    <a href="{url}" style="color:#4f46e5;font-size:14px;
                                          font-weight:500;text-decoration:none;">
                      {dash(website_key)}
                    </a>
                  </td>
                </tr>

                
                <tr>
                  <td style="padding:14px 16px;background-color:#f8faff;
                             border-right:1px solid #e2e8f0;
                             border-bottom:1px solid #e2e8f0;vertical-align:middle;">
                    <span style="color:#94a3b8;font-size:11px;font-weight:700;
                                 letter-spacing:1px;text-transform:uppercase;">Product</span>
                  </td>
                  <td style="padding:14px 18px;border-bottom:1px solid #e2e8f0;
                             vertical-align:middle;background-color:#ffffff;">
                    <span style="color:#334155;font-size:14px;">{dash(product)}</span>
                  </td>
                </tr>

                
                <tr>
                  <td style="padding:14px 16px;background-color:#f8faff;
                             border-right:1px solid #e2e8f0;
                             border-bottom:1px solid #e2e8f0;vertical-align:middle;">
                    <span style="color:#94a3b8;font-size:11px;font-weight:700;
                                 letter-spacing:1px;text-transform:uppercase;">Product Type</span>
                  </td>
                  <td style="padding:14px 18px;border-bottom:1px solid #e2e8f0;
                             vertical-align:middle;background-color:#ffffff;">
                    <span style="color:#334155;font-size:14px;">{dash(product_type)}</span>
                  </td>
                </tr>

                
                <tr>
                  <td style="padding:14px 16px;background-color:#f8faff;
                             border-right:1px solid #e2e8f0;
                             border-bottom:1px solid #e2e8f0;vertical-align:middle;">
                    <span style="color:#94a3b8;font-size:11px;font-weight:700;
                                 letter-spacing:1px;text-transform:uppercase;">IP Address</span>
                  </td>
                  <td style="padding:14px 18px;border-bottom:1px solid #e2e8f0;
                             vertical-align:middle;background-color:#ffffff;">
                    <span style="color:#334155;font-size:14px;">{dash(ip_address)}</span>
                  </td>
                </tr>

                
                <tr>
                  <td style="padding:14px 16px;background-color:#f8faff;
                             border-right:1px solid #e2e8f0;vertical-align:top;">
                    <span style="color:#94a3b8;font-size:11px;font-weight:700;
                                 letter-spacing:1px;text-transform:uppercase;">Message</span>
                  </td>
                  <td style="padding:16px 18px;vertical-align:top;background-color:#ffffff;">
                    <p style="margin:0;color:#334155;font-size:14px;line-height:1.8;
                               border-left:3px solid #6366f1;padding-left:14px;font-style:italic;">
                      {message if message else "No message provided."}
                    </p>
                  </td>
                </tr>

              </table>

              
              <table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:28px;">
                <tr><td style="height:1px;background-color:#e2e8f0;"></td></tr>
              </table>

              
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td align="center">
                    <table cellpadding="0" cellspacing="0">
                      <tr>
                        <td style="padding-right:12px;">
                          <a href="mailto:{email}?subject=Re%3A%20Your%20Inquiry"
                             style="display:inline-block;padding:14px 30px;
                                    border-radius:100px;background-color:#4f46e5;
                                    color:#ffffff;text-decoration:none;
                                    font-size:14px;font-weight:700;">
                            Reply to {name} 
                          </a>
                        </td>
                        <td>
                          <a href="{url}"
                             style="display:inline-block;padding:13px 26px;
                                    border-radius:100px;background-color:#ffffff;
                                    color:#4f46e5;text-decoration:none;
                                    font-size:14px;font-weight:700;
                                    border:2px solid #4f46e5;">
                            View Site
                          </a>
                        </td>
                      </tr>
                    </table>
                  </td>
                </tr>
              </table>

            </td>
          </tr>
        </table>

        
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td style="height:4px;background-color:#ec4899;"></td>
            <td style="height:4px;background-color:#8b5cf6;"></td>
            <td style="height:4px;background-color:#6366f1;"></td>
          </tr>
        </table>

      </td>
    </tr>

    
    <tr>
      <td style="padding:22px 0;text-align:center;">
        <p style="margin:0;color:#94a3b8;font-size:12px;line-height:1.7;">
          Automated notification from
          <a href="{url}" style="color:#64748b;text-decoration:none;">{lbl}</a>
          &nbsp;&nbsp;  {year}
        </p>
      </td>
    </tr>

  </table>
</td></tr>
</table>
</body>
</html>"""

