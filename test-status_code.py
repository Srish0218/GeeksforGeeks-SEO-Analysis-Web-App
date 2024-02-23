import requests
page = requests.get("https://www.ibm.com/academic/topic/data-science")
print(page.status_code)

"""

Testing the status code of a website is crucial before performing SEO analysis for a few reasons:

1. **Validating URL Existence:** By checking the status code, you ensure that the provided URL is reachable and 
exists. If the URL returns a 404 Not Found or another error status code, it means the webpage doesn't exist, 
and attempting SEO analysis on a non-existent page would be pointless.

2. **Handling Redirections:** Websites might use redirects (e.g., 301 or 302 status codes) to forward users from one 
URL to another. Checking the status code helps you follow these redirects and analyze the content of the final 
destination page.

3. **Error Handling:** If the status code is outside the 200-299 range (commonly successful responses), it indicates 
an issue with accessing the webpage. By checking and handling these error status codes, you can provide more 
informative messages to users, helping them understand and troubleshoot any issues.

In the provided Streamlit app code, the `requests.get(url)` call is followed by checking the status code with `if 200 
<= page.status_code < 300:`. If the status code is not in the success range, a warning is displayed, and the analysis 
is not performed, preventing potential issues caused by trying to analyze content from a problematic webpage.

"""