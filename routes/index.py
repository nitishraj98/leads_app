from flask import Blueprint, render_template_string

index_bp = Blueprint("index", __name__)

FORM_HTML = """<!DOCTYPE html><html><head><title>Contact Form</title>
<style>
  body{font-family:Arial,sans-serif;max-width:520px;margin:60px auto;padding:20px;}
  label{font-size:13px;font-weight:600;color:#444;}
  input,textarea{width:100%;padding:10px;margin:6px 0 16px;border:1px solid #ddd;
                 border-radius:8px;box-sizing:border-box;font-size:14px;}
  button{background:linear-gradient(135deg,#6366f1,#14b8a6);color:white;
         padding:13px 28px;border:none;border-radius:8px;
         cursor:pointer;font-size:15px;font-weight:600;}
  button:hover{opacity:0.9;}
  #msg{margin-top:16px;padding:12px;border-radius:8px;display:none;}
  .success{background:#d4edda;color:#155724;}
  .error{background:#f8d7da;color:#721c24;}
</style></head>
<body>
<h2>Contact Us</h2>
<label>Name *</label>
<input type="text"  id="name"         placeholder="Your full name">
<label>Email *</label>
<input type="email" id="email"        placeholder="you@example.com">
<label>Phone</label>
<input type="tel"   id="phone"        placeholder="+1 234 567 890">
<label>Product</label>
<input type="text"  id="product"      placeholder="e.g. CRM Software">
<label>Product Type</label>
<input type="text"  id="product_type" placeholder="e.g. Enterprise / SaaS">
<label>Message</label>
<textarea           id="message" rows="4" placeholder="Your message..."></textarea>
<label>Website Key</label>
<input type="text"  id="website_key"  placeholder="https://yourwebsite.com">

<!-- Honeypot (hidden from real users) -->
<input type="text" id="company" style="display:none;" tabindex="-1" autocomplete="off">

<button onclick="submitForm()">Submit</button>
<div id="msg"></div>

<script>
async function submitForm() {
  const btn = document.querySelector('button');
  btn.disabled = true;
  btn.textContent = 'Sending…';

  const res = await fetch('/submit', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
      name:         document.getElementById('name').value,
      email:        document.getElementById('email').value,
      phone:        document.getElementById('phone').value,
      product:      document.getElementById('product').value,
      product_type: document.getElementById('product_type').value,
      message:      document.getElementById('message').value,
      website_key:  document.getElementById('website_key').value,
      company:      document.getElementById('company').value,   // honeypot
    })
  });

  const data = await res.json();
  const el = document.getElementById('msg');
  el.style.display = 'block';
  el.className = data.success ? 'success' : 'error';
  el.textContent = data.message;

  if (data.success) {
    ['name','email','phone','product','product_type','message','website_key']
      .forEach(id => document.getElementById(id).value = '');
  }
  btn.disabled = false;
  btn.textContent = 'Submit';
}
</script>
</body></html>"""


@index_bp.route("/")
def index():
    return render_template_string(FORM_HTML)
