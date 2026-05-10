# Multiverse Discord Bot

A Discord bot that interconnects multiple servers through a shared `#multiverse` channel using webhooks.  
Messages sent in one multiverse channel are automatically forwarded to all connected servers.  
The bot includes anti-spam protection, automatic temporary blacklist handling, permanent blacklist controls, and link blocking inside multiverse channels.  
Attachments are also forwarded while preserving usernames and avatars through webhooks.  
Built using `discord.py` with slash commands support.

---

# Features

- Cross-server chat system
- Automatic multiverse channel setup
- Webhook-based message forwarding
- Username and avatar preservation
- Attachment forwarding
- Repetition spam detection
- Automatic temporary blacklist
- Permanent blacklist system
- Unblacklist system
- Link blocking inside multiverse
- Slash command support

---

# Commands

| Command | Function |
|---|---|
| `/setup_multiverse` | Creates the `#multiverse` channel and webhook |
| `/blacklist user_id` | Permanently blacklists a user from multiverse |
| `/unblacklist user_id` | Removes user from blacklist |

---

# Special Notes

- Link blocking only applies inside `#multiverse`
- Repeated spam messages trigger automatic temporary blacklist
- Attachments are forwarded between linked servers
- Webhooks preserve sender username and avatar
- Requires `Manage Channels` and `Manage Webhooks` permissions
Example:-
<img width="450" height="238" alt="image" src="https://github.com/user-attachments/assets/e0286006-cbe9-469b-9956-b0cb2fcb93ca" />

## 🧭 Summary

This bot creates a **shared chat network across servers**, making multiple communities feel like one unified space.
