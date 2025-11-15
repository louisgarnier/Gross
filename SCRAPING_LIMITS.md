# Scraping Limits & Best Practices

## ⚠️ Important: This is Web Scraping, Not an Official API

This application uses **web scraping** to extract data from financial websites. This is different from using an official API.

### What is Web Scraping?
- Making HTTP requests to websites
- Parsing HTML to extract data
- **No official permission** from the website
- Can be blocked or rate-limited

### Rate Limiting Protection

We've implemented several protections:

1. **Request Delays**: Minimum 2 seconds between requests to the same website
2. **Caching**: Results cached for 1 hour to avoid repeated requests
3. **Retry Logic**: Exponential backoff on errors
4. **User-Agent**: Proper browser identification

### Limitations

**Finviz and other sites may:**
- Block your IP if you make too many requests
- Rate limit requests (slow down or block)
- Change HTML structure (breaking scrapers)
- Require authentication/captcha

### Best Practices

1. **Don't test too frequently**: Wait between tests
2. **Use caching**: Same ticker won't be scraped again for 1 hour
3. **Respect delays**: The scraper automatically waits 2 seconds between requests
4. **Monitor for blocks**: If you get errors, wait before retrying

### If You Get Blocked

If you see errors like:
- `403 Forbidden`
- `429 Too Many Requests`
- Timeouts
- Empty results

**Solutions:**
1. Wait 10-15 minutes before retrying
2. Clear cache: Restart the backend server
3. Use a VPN (if IP is blocked)
4. Reduce testing frequency

### Cache Management

The cache stores results for 1 hour. To clear:
- Restart the backend server
- Or wait 1 hour for automatic expiration

### Development vs Production

**Development (now):**
- Testing with a few tickers is fine
- Cache helps avoid repeated requests
- 2-second delay is sufficient

**Production (later):**
- Consider longer cache times (4-6 hours)
- May need to increase delays
- Monitor for blocks
- Consider using official APIs if available

---

## Current Implementation

- ✅ Rate limiting: 2 seconds between requests
- ✅ Caching: 1 hour TTL
- ✅ Retry logic: 3 attempts with exponential backoff
- ✅ Proper User-Agent headers

**Status**: Safe for development/testing. Be mindful of request frequency.

