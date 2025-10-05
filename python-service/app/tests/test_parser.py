# test_parser.py
from app.fetcher.parser import parse_int_from_text, parse_money, job_from_card_html

def test_parse_int():
    assert parse_int_from_text("12 proposals") == 12
    assert parse_int_from_text("no proposals") == 0
    assert parse_int_from_text("1,234 proposals") == 1234

def test_parse_money():
    assert parse_money("$1,200") == 1200.0
    assert parse_money("€2,500.50 monthly") == 2500.50

def test_job_from_card_html_simple():
    html = '''
    <article class="job-tile">
      <a href="https://upwork.com/job/123"><h4>Scrape product list</h4></a>
      <div class="snippet">Extract product title, price, sku</div>
      <div class="proposals-count">3 proposals</div>
      <div class="budget">$200</div>
      <div class="tag">python</div>
      <div class="client"><span class="payment-verified">Verified</span><span class="hire-rate">75%</span></div>
    </article>
    '''
    job = job_from_card_html(html)
    assert job["title"].lower().startswith("scrape")
    assert job["proposals_count"] == 3
    assert job["budget_amount"] == 200.0
    assert "python" in job["required_skills"]

