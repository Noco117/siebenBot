import discord

token = "xyz"
forced_channel_ids = [996928095372185700, 1014956223768035369, 1010674929026469939, 1282087971662729248]  # List of all Channels that "sieben" is strictly enforced in
#                                           # Currently only includes sieben in GENERAL and TALKI WALKI and
#                                           # ebenfalls sieben also in TALKI WALKI and Taverne banannnnnnna # sieben in General (not the category but rather ungrouped)


class SiebenClient(discord.Client):

    async def on_voice_state_update(self, member, before, after):
        if after.channel is None:
            return

        if before.channel is not after.channel and len(after.channel.members) == 1:
            await after.channel.set_status("sieben")

    async def on_voice_channel_status_update(self, channel, before, after):
        if channel.id in forced_channel_ids and channel.members and after != "sieben":
            await channel.set_status("sieben")


client = SiebenClient()
client.run(token)
