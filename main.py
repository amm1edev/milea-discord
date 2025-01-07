import sys
import discord
import requests
import random
from asyncio import sleep
from discord.ext import commands
from typing import Optional
from config import *

#sys.__version__
#discord.__version__

intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix='n.', intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    await bot.change_presence(status=discord.Status.online, activity=discord.Game("Спасибо, кто использует бота!"))
    await bot.tree.sync()

#clear
@bot.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount: int = 10):
    user = ctx.author
    userid = ctx.author.id
    embed = discord.Embed(
        title='Успешно!',
        description=f'<:clearicon:1085890319058472970> **Было очищено** `{amount}` **сообщений/ия**',
        color=discord.Color.magenta())
    embed.set_footer(text=str(userid) + ' | ' + str(user))
    error = discord.Embed(
        title = '<:error:1085891108267118622>  Ошибка!',
        description = 'Количество удаляемых сообщений **является отрицательным**',
        color = discord.Color.red())
    if amount >= 0:
        await ctx.channel.purge(limit = amount)
        await ctx.send(embed=embed)
        await sleep(15)
        await ctx.channel.purge(limit = 1)
    else:
        await ctx.send(embed=error)
        await sleep(15)
@clear.error
@commands.has_permissions(manage_messages = False)
async def clear_error(ctx: commands.Context, error: commands.CommandError):
    error = discord.Embed(
        title = '<:error:1085891108267118622> Ошибка!',
        description = '**Возможные причины:** \n\n > Был пропущен или неккоректно введен аргумент.\n > У вас нет прав на `управление сообщениями`\n > У бота нет прав на `управление сообщениями`\n\n<:icon:1085892326653706290> ***Если это не так обратитесь в поддержку -*** `n.botinfo`',        color = discord.Color.red())
    await ctx.send(embed=error)

# test button
@bot.command()
async def testcom(ctx):
    emb = await ctx.send(discord.Embed(title='test', components = [Button(style = ByttonStyle.blue, label = 'test')]))
# slowmode
@bot.command()
@commands.has_permissions(manage_channels = True)
async def slowmode(ctx, delay: int = None):
    if delay < 0:
        embed = discord.Embed(
            title = "<:error:1085891108267118622> Ошибка!",
            description = "Количество удаляемых сообщений не может быть отрицательным",
            color = discord.Color.red())
        await ctx.send(embed=embed)
    elif delay > 21600:
        embed = discord.Embed(
            title = "<:error:1085891108267118622> Ошибка!",
            description = "Нельзя использовать время больше 6ч",
            color = discord.Color.red())
        await ctx.send(embed=embed)
    elif delay >= 0:
        embed = discord.Embed(
            title='Успешно!',
            description=f'<:clearicon:1085890319058472970> Был поставлен слоумод на {delay} секунд',
            color=discord.Color.magenta())
        await ctx.send(embed=embed)
        await ctx.channel.edit(
            slowmode_delay = delay,
            reason = f"{ctx.author.name} | {ctx.author.id} | milea")
@slowmode.error
@commands.has_permissions(manage_channels = False)
async def slowmode_error(ctx: commands.Context, error: commands.CommandError):
    error = discord.Embed(
        title = '<:error:1085891108267118622> Ошибка!',
        description = '**Возможные причины:** \n\n > Вы пропустили аргумент\n > У вас нет прав на `управление каналами`\n > У бота нет прав на `управление каналами`\n\n<:icon:1085892326653706290> ***Если это не так обратитесь в поддержку -*** `n.botinfo`',        color = discord.Color.red())
    await ctx.send(embed=error)


# avatar
@bot.command()
async def avatar(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    embed = discord.Embed(
        title=f"Аватар {member.name}",
        description=f'**Аватар пользователя** `{member.name}` \n\n[Нажмите что бы скачать]({member.avatar})',
        color=discord.Color.magenta()
    )
    embed.set_thumbnail(url=member.avatar)
    await ctx.send(embed=embed)


#say
@bot.command()
async def say(ctx, *, turple):
    user = ctx.author
    userid = ctx.author.id
    embed = discord.Embed(description=turple, color=discord.Color.magenta())
    embed.set_footer(text=str(userid) + ' | ' + str(user))
    await ctx.channel.send(embed=embed)
    await ctx.message.delete()
@say.error
async def say_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        error = discord.Embed(
            title = '<:error:1085891108267118622> Ошибка!',
            description = 'Был пропущен аргумент!',
            color = discord.Color.red())
        await ctx.send(embed=error)

#/help
@bot.tree.command(description="Список всех команд")
async def help(interaction: discord.Interaction):
    embed = discord.Embed(
        title='Помощь',
        description='<:moderation:1084336438922977340> **Модерация:** \n' +
        '> **n.server** -  Получить информацию о сервере\n' +
        '> **n.clear <число>** - Удалить N сообщений (по умолчанию - 10)\n' +
        '> **n.slowmode <число>** - Поставить слоумод в канале (0 - убрать его)\n' +
        '> **n.whcreate <название вебхука>** - Создать вебхук\n\n' +
        '<:funny:1084336437027164240> **Веселости:** \n' +
        '> **n.ball <вопрос>** - Получить рандомный ответ на ваш вопрос\n' +
        '> **n.avatar <@участник>** - Получить аватар пользователя\n' +
        '> **n.hug <@участник>** - Обнять пользователя :3\n\n' +
        '<:other:1084336441917718578> **Другое:**\n' +
        '> **n.idea <идея>** - Отправить идею для бота\n' +
        '> **n.say <текст>** - Отправить сообщение от имени бота\n' +
        '> **n.botinfo** - Информация о боте\n' +
        '> **n.userinfo <@пользователь>** - Информация о пользователе',
        color=discord.Color.magenta()
        )
    embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/1084437072124850296.webp?size=48&quality=lossless')
    await interaction.response.send_message(embed=embed)

@bot.event
async def on_guild_join(guild: discord.Guild):
    channel = bot.get_channel(1084891297342570667)
    embed = discord.Embed(
        title="Новый сервер!",
        color=discord.Color.green()
    )
    if guild.icon is not None:
        embed.set_image(url=guild.icon.url)
    embed.add_field(name="Название:", value=guild.name)
    embed.add_field(name="ID:", value=guild.id)
    embed.add_field(name="Создатель:", value=guild.owner)
    await channel.send(embed=embed)

#ball
@bot.command()
async def ball(ctx, *, turple):
    user = ctx.author
    userid = ctx.author.id
    answers = [
        "да", "нет", "не знаю что сказать", "скорее всего", "вряд ли", "не думаю",
        "обязательно", "спроси еще раз"
    ]
    answer = random.choice(answers)
    embed = discord.Embed(
        title='Магический шар(Нет)',
        description='**Вопрос:** ' + turple + '\n' +
        '**Мой ответ:** ' + answer,
        color=discord.Color.magenta())
    embed.set_footer(text=str(userid) + ' | ' + str(user))
    await ctx.channel.send(embed=embed)

#whcreate
@bot.command()
@commands.has_permissions(manage_webhooks = True)
async def whcreate(ctx, *, arg):
    webhook = await ctx.channel.create_webhook(name=arg)
    embed = discord.Embed(
        title='<:clearicon:1085890319058472970> Создание вебхука',
        description=f'**Название вебхука: ** `{arg}`\nURL вебхука был отправлем вам в лс', 
        color=discord.Color.magenta())
    embed2 = discord.Embed(
        title='Webhook URL',
        description=f'{webhook.url}',
        color=discord.Color.magenta())

    await ctx.channel.send(embed=embed)
    await ctx.author.send(embed=embed2)
@whcreate.error
@commands.has_permissions(manage_webhooks = False)
async def idea_error(ctx: commands.Context, error: commands.CommandError):
    error = discord.Embed(
        title = '<:error:1085891108267118622> Ошибка!',
        description = '**Возможные причины:** \n\n > У вас нет прав на `Управление вебхуками`,\n> У бота нет прав на `Управление вебхуками`,\n> Вы пропустили аругмент. \n\n<:icon:1085892326653706290> ***Если это не так обратитесь в поддержку -*** `n.botinfo`',
        color = discord.Color.red())
    await ctx.channel.send(embed=error)
    
    
#test
@bot.command()
async def test(ctx, member: discord.Member = None):
    ping = int(round(bot.latency, 3)*1000)
    cos = len(bot.guilds)
    com = value=len(bot.users)
    if member.guild_permissions.administrator:
        adm = str('1')
    else:
        adm = str('0')
    stats = discord.Embed(title=f"milea - debug", color=discord.Color.magenta())
    stats.set_footer(text=f'{int(round(bot.latency, 3)*1000)}.{cos}.{com}.{adm}')
    await ctx.send(embed=stats)



#idea
@bot.command()
async def idea(ctx, *, var):
    channel = bot.get_channel(1069891396951101490)
    user = ctx.author
    userid = ctx.author.id
    embed2 = discord.Embed(title='Идея отправлена',
        description=f'**Содержание: **' + "   " + var,
        color=discord.Color.magenta()
    )
    embed = discord.Embed(title='Новая идея!',
        description="От - " + "**" + str(user) + "** " + '\n' +
        f'> **Содержание: **' + var,
        color=discord.Color.magenta()
    )
    embed.set_footer(text=str(userid) + ' | ' + str(user))
    await channel.send(embed=embed)
    await ctx.channel.send(embed=embed2)
@idea.error
async def idea_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        error = discord.Embed(
            title = '<:error:1085891108267118622> Ошибка!',
            description = 'Был пропущен аргумент!',
            color = discord.Color.red())
        await ctx.send(embed=error)

#hug
@bot.command()
async def hug(ctx, member: discord.User):
    response = requests.get('https://some-random-api.ml/animu/hug')
    data = response.json()
    user = ctx.author.id
    user1 = ctx.author
    if member.id == user:
        error1 = discord.Embed(
            title = 'Ошибка!',
            description = 'Нельзя обнять самого себя!',
            color = discord.Color.red())
        await ctx.send(embed=error1)
        await ctx.message.delete()
    elif member.bot:
        error2 = discord.Embed(
            title = 'Ошибка!',
            description = 'Нельзя обнять бота!',
            color = discord.Color.red())
        await ctx.send(embed=error2)
        await ctx.message.delete()
    elif user != member.id:
        embed = discord.Embed(
            title=f'{user1} обнял {member}!',
            color=discord.Color.magenta())
        embed.set_image(url=data['link'])
        await ctx.send(embed=embed)
        await ctx.message.delete()
    else:
        await ctx.send('Error')
@hug.error
async def idea_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        error = discord.Embed(
            title = '<:error:1085891108267118622> Ошибка!',
            description = '**Возможные причины:** \n\n > Был пропущен аргумент.\n\n<:icon:1085892326653706290> ***Если это не так обратитесь в поддержку -*** `n.botinfo`',
            color = discord.Color.red())
        await ctx.send(embed=error)
 
#help
@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title='Помощь',
        description='<:moderation:1084336438922977340> **Модерация:** \n' +
        '> **n.server** -  Получить информацию о сервере\n' +
        '> **n.clear <число>** - Удалить N сообщений (по умолчанию - 10)\n' +
        '> **n.slowmode <число>** - Поставить слоумод в канале (0 - убрать его)\n' +
        '> **n.whcreate <название вебхука>** - Создать вебхук\n\n' +
        '<:funny:1084336437027164240> **Веселости:** \n' +
        '> **n.ball <вопрос>** - Получить рандомный ответ на ваш вопрос\n' +
        '> **n.avatar <@участник>** - Получить аватар пользователя\n' +
        '> **n.hug <@участник>** - Обнять пользователя :3\n\n' +
        '<:other:1084336441917718578> **Другое:**\n' +
        '> **n.idea <идея>** - Отправить идею для бота\n' +
        '> **n.say <текст>** - Отправить сообщение от имени бота\n' +
        '> **n.botinfo** - Информация о боте\n' +
        '> **n.userinfo <@пользователь>** - Информация о пользователе',
        color=discord.Color.magenta())
    embed.set_thumbnail(url='https://cdn.discordapp.com/emojis/1084437072124850296.webp?size=48&quality=lossless')
    await ctx.channel.send(embed=embed)
   

#ping > botinfo
@bot.command()
async def botinfo(ctx):
    user = ctx.author
    userid = ctx.author.id
    ping = bot.ws.latency
    embed = discord.Embed(
        title="<:chat:1084437072124850296> | Информация о боте",
        description=f'<:ping:1085899228905230366> | **Пинг:** {ping * 1000:.0f}ms\n' +
        '<:srvs:1085899231870586900> | **Количество серверов:** ' + str(len(bot.guilds)) + '\n' + '\n' +
        '<:support:1085899233841905755> | **Разработчики:** \n <@777140702747426817> (id: 777140702747426817)\n' +
        '\n' + f'<:langprgr:1085899240674426962> | **Язык программирования:** Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}\n' +
        f'<a:langprgr2:1085899237469995058> | **Библиотека:** discord.py {discord.__version__}\n\n' +
        '<:support:1085899233841905755> | **Поддержка -** https://discord.gg/JCv9jUk8Ku',
        color=discord.Color.magenta()
    )
    embed.set_footer(text=str(userid) + " | " + str(user))
    await ctx.send(embed=embed)

#userinfo
@bot.command()
async def userinfo(ctx, member: discord.Member = None):
    if member == None:
        member = ctx.author
    bages = ''
    if member.id in owner:
        bages += '<:ownerbot:1085879574417637376> '
    if member.id in partner:
        bages += '<a:partner:1085877042685415454> '
    if member.id in vip:
        bages += '<:vip:1085877047836037161> '
    if member.id in bughunter:
        bages += '<:bughanter:1085877039531302922> '
    
    embed = discord.Embed(color=member.color, title=f"**Информация о пользователе** `{member}` | {bages}", description=f"**Аватар:** [Скачать]({member.display_avatar.replace(static_format='png', size=2048)})")
    embed.set_thumbnail(url=member.avatar)
    embed.set_author(name='')
    embed.set_footer(text=f'{ctx.author} | {ctx.author.id}')

    embed.add_field(name='**Айди:** ', value=member.id, inline=False)
    embed.add_field(name='**Никнейм:** ', value=member.display_name, inline=False)

    embed.add_field(name='**Аккаунт создан:** ', value=f"{discord.utils.format_dt(member.created_at, 'D')} ({discord.utils.format_dt(member.created_at, 'R')})", inline=False)
    embed.add_field(name='**Зашел на сервер:** ', value=f"{discord.utils.format_dt(member.joined_at, 'D')} ({discord.utils.format_dt(member.joined_at, 'R')})", inline=False)

    if member.bot:
        embed.add_field(name="Бот?:", value="Да", inline=False)
    else:
        embed.add_field(name="Бот?:", value="Нет", inline=False)

    if member.guild_permissions.administrator:
        embed.add_field(name="Администратор?:", value='Да', inline=False)
    else:
        embed.add_field(name="Администратор?:", value='Нет', inline=False)

    embed.add_field(name="Самая высокая роль на сервере:", value=f"{member.top_role.mention}", inline=False)
    user_banner = await bot.fetch_user(member.id)
    user_banner = user_banner.banner
    if user_banner is not None:
        embed.set_image(url=user_banner.url)
    await ctx.send(embed=embed)
@userinfo.error
async def userinfo_error(ctx: commands.Context, error: commands.CommandError):
    if isinstance(error, discord.ext.commands.errors.MemberNotFound):
        error = discord.Embed(
            title = '<:error:1085891108267118622> Ошибка!',
            description = '**Возможные причины:** \n\n > Был неккоректно введен аргумент.\n\n<:icon:1085892326653706290> ***Если это не так обратитесь в поддержку -*** `n.botinfo`',
            color = discord.Color.red())
        await ctx.channel.send(embed=error)
    

# server
@bot.command()
async def server(ctx):
    user = ctx.author
    userid = ctx.author.id
    all = len(ctx.guild.members)
    bot = 0
    for i in ctx.guild.members:
        if i.bot:
            bot +=1
    members = int(all) - int(bot)
    emoji = 0
    anim_emoji = 0
    for gfdd in ctx.guild.emojis:
        if gfdd.animated == True:
            anim_emoji += 1
        elif gfdd.animated == False:
            emoji += 1
    online = 0
    idle = 0
    offline = 0
    dnd = 0

    text = 0
    voice = 0

    static_emoji = int(emoji) - int(anim_emoji)
    for member in ctx.guild.members:
        if str(member.status) == "online":
            online += 1
        if str(member.status) == "idle":
            idle += 1
        if str(member.status) == "dnd":
            dnd += 1
        if str(member.status) == "offline":
            offline += 1
    for channel in ctx.guild.channels:
        if str(channel.type) == "text":
            text += 1
        if str(channel.type) == "voice":
            voice += 1
    owner = ctx.guild.owner.mention
  
    embed = discord.Embed(
        title="Информация о сервере:",
        description=f"> <:allusers:1084437064449273956> **Всего участников:** {all}\n" +
        f"> <:users:1084437092307837048> **Участников:** {members}\n" + f"> <:bots:1084437069276925982> **Ботов: ** {bot}" + "\n" + "\n" +
        f"> <:chat:1084437072124850296> **Текстовых каналов:** {text}\n" +
        f"> <:voice:1084437095222890506> **Голосовых каналов:** {voice}\n" + "\n" +
        f"> <:emojis:1084437077128646686> **Эмодзи:** {emoji}\n" +
        f"> <:animrmoij:1084437067154604055> **Анимированных эмодзи:** {anim_emoji}\n" +
        f"> <:stemoji:1084437090374275172> **Статических эмодзи:** {static_emoji}\n" + "\n" +
        f"> <:online:1084437085580173402> **Онлайн:** {online}\n" + f"> <:dnd:1084437073903226910> **Не на месте:** {idle}\n" +
        f"> <:inactive:1084437079112548383> **Неактивен:** {dnd}\n" + f"> <:offline:1084437082262474883> **Оффлайн:** {offline}\n" + "\n" +
        f"> <:owner:1084437087090122773> **Владелец:** {owner}",
        color=discord.Color.magenta()
        )
    embed.set_footer(text=str(userid) + " | " + str(user))
    await ctx.channel.send(embed=embed)

bot.run(settings['token'])
status =(["https://t.me/m1lkaa_a"])

