import discord
from discord.ext import commands

class Moderation(commands.Cog):
    """Cog for moderation-ish commands such as banning or clearing"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        """Clears {amount} messages"""
        logchannel = self.bot.get_channel(848362560255950888)
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f":+1: {amount} messages deleted", delete_after=3)
        await logchannel.send(f"<:bin:848554827545444402> - {amount} messages deleted in **`{ctx.guild}`**")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, days=None, *, reason=None):
        """Bans the mentioned member"""
        await member.ban(reason=reason, delete_message_days=days)
        await ctx.send(f"{member.mention} was banned for `{reason}`")
        logchannel = self.bot.get_channel(848362560255950888)
        await logchannel.send(f"<:empty:848375084577325068> - **{member.mention}** was banned from **`{ctx.guild}`** for `{reason}`")

    @commands.command()
    @commands.has_permissions(ban_members=True, kick_members=True)
    async def unban(self, ctx, *, member):
        """Unbans the mentioned member"""
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"**`{user.name}#{user.discriminator}`** was unbanned")

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason):
        """Kicks the mentioned member"""
        await member.kick(reason=reason)
        await ctx.send(f"{member.mention} was kicked for `{reason}`")
        logchannel = self.bot.get_channel(848362560255950888)
        await logchannel.send(f"<:empty:848375084577325068> - **{member.mention}** was kicked from **`{ctx.guild}`** for `{reason}`")

    @commands.command()
    @commands.has_permissions(kick_members=True, manage_roles=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        """Mutes the mentioned member
        nt,he only"""
        if ctx.guild.id != 804449200921509913:
            return
        if reason == None:
            reason = "No reason specified"
        muterole = discord.utils.get(ctx.guild.roles, name="muted")
        if muterole in member.roles:
            await ctx.send(f"{member.mention} is already muted.")
            return
        else:
            await member.add_roles(muterole, reason=reason)
            logchannel = self.bot.get_channel(848362560255950888)
            await ctx.send(f"{member.mention} was just muted for `{reason}`")
            await logchannel.send(f"<:empty:848375084577325068> - **{member.mention}** was muted for `{reason}`")
            return
    
    @commands.command()
    @commands.has_permissions(kick_members=True, manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        """Unmutes the mentioned member
        nt,he only"""
        if ctx.guild != 804449200921509913:
            return
        muterole = discord.utils.get(ctx.guild.roles, name="muted")
        if muterole in member.roles:
            await member.remove_roles(muterole)
            logchannel = self.bot.get_channel(848362560255950888)
            await ctx.send(f"{member.mention} was just unmuted")
            await logchannel.send(f"<:empty:848375084577325068> - **{member.mention}** was unmuted")
            return
        else:
            await ctx.send(f"{member.mention} isn't muted.")
            return

def setup(bot):
    bot.add_cog(Moderation(bot))