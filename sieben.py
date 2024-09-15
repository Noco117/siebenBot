import discord
import config
import botsettings
from datetime import timedelta, datetime

disallowed_status_components = botsettings.disallowed_status_components
allowed_exceptions = botsettings.allowed_exceptions
accepted_sieben_strings = botsettings.accepted_sieben_strings
timeout_reason = botsettings.timeout_reason
overprivileged_member_message = botsettings.overprivileged_member_message


class SiebenClient(discord.Client):

    async def is_valid_status(self, channel: discord.VoiceChannel, status: str) -> bool:
        if status is None:
            return True if "sieben" not in channel.name else False
        if status in allowed_exceptions:
            return True
        for item in disallowed_status_components:
            if item in status:
                async for entry in channel.guild.audit_logs(limit=1,
                                                            action=discord.AuditLogAction.voice_channel_status_update):
                    if channel.guild.me.top_role > entry.user.top_role and not channel.guild.owner_id == entry.user.id:
                        await entry.user.timeout(until=(datetime.utcnow() + timedelta(seconds=20)),
                                                 reason=timeout_reason)
                    else:
                        await entry.user.send(overprivileged_member_message)
                return False

        if "sieben" in channel.name:
            return status in accepted_sieben_strings

        return True

    async def on_voice_state_update(self, member, before, after):
        print("update")
        if after.channel is None:
            return

        if before.channel is not after.channel and len(after.channel.members) == 1:
            await after.channel.set_status("sieben")

    async def on_voice_channel_status_update(self, channel, before, after):
        if (not await self.is_valid_status(channel, after)) and channel.members:
            print("siebened")
            await channel.set_status("sieben")


client = SiebenClient()
client.run(config.TOKEN)
