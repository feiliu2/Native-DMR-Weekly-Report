# How to Get Artifactory API Token

## Quick Steps

### 1. Login to Artifactory

Open your browser and navigate to:
```
https://af01p-or.devtools.intel.com/
```

**Login with your Intel credentials**

---

### 2. Access Your Profile

After login:
1. Look at the **top right corner** of the page
2. Click on your **username**
3. From the dropdown menu, select **"Edit Profile"**

---

### 3. Generate API Key

In your Edit Profile page:

1. Scroll down to find the **"API Key"** section
2. You will see either:
   - **Option A: First Time (No API Key Yet)**
     - Click **"Generate API Key"** button
     - Your token will be displayed (starts with `AKCp...`)
   
   - **Option B: Already Have a Key (Regenerate)**
     - Click **"Regenerate"** button
     - Confirm the regeneration
     - New token will be displayed (old one will be invalidated)

---

### 4. Copy the Token

- **Format:** `AKCp8ohx...` (long alphanumeric string)
- **Length:** ~40-60 characters
- **Important:** Copy the entire token

Example:
```
AKCp8ohxzGaM7p4vAMCt5HoM7B5N3aJ65Wdv1HzY
```

---

### 5. Use the Token

Paste the token when the PowerShell script prompts:
```
Enter Artifactory API Token: ****************
```

---

## Security Notes

⚠️ **Keep Your Token Secure:**
- Do NOT share your API token with others
- Do NOT commit tokens to Git repositories
- Do NOT post tokens in public channels (Slack, Teams, etc.)

✅ **Token Permissions:**
- Your API token has the same permissions as your user account
- Only access Artifactory resources you have permission to view

🔄 **Token Expiration:**
- Tokens may expire based on company policy
- If authentication fails (HTTP 403), regenerate a new token

---

## Troubleshooting

### Error: HTTP 403 (Authentication Failed)

**Possible causes:**
1. Token expired → Regenerate new token
2. Token copied incorrectly → Check for extra spaces or missing characters
3. Insufficient permissions → Contact Artifactory admin

**Solution:**
- Go back to User Profile
- Regenerate API Key
- Copy the new token completely
- Try again

---

### Error: HTTP 401 (Unauthorized)

**Possible causes:**
1. No token provided
2. Empty or invalid token format

**Solution:**
- Make sure you pasted the complete token
- Token should start with `AKCp`

---

### Cannot Access User Profile Page

**Possible causes:**
1. Not logged into Intel network/VPN
2. Artifactory service down

**Solution:**
- Connect to Intel network or VPN
- Try accessing: `https://af01p-or.devtools.intel.com/`
- If site is unreachable, check network connection

---

## Alternative: Using Password Authentication

If API Token doesn't work, you can use username/password:

**Base64 Encoding:**
```bash
echo -n "username:password" | base64
```

**Use in Header:**
```
Authorization: Basic <base64_encoded_credentials>
```

However, **API Token is recommended** for better security.

---

## Reference Links

- **Artifactory User Profile:**
  ```
  https://af01p-or.devtools.intel.com/ui/admin/artifactory/user_profile
  ```

- **Intel Artifactory Help:**
  - Contact IT support if you cannot access Artifactory
  - Check internal wiki for Artifactory documentation

---

**Last Updated:** 2026-06-30
