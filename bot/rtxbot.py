import json
from discord.ext import commands, tasks
from requests import Session
from requests.exceptions import RequestException

class RTXBot(commands.Cog):
    """
    A custom Discord bot for monitoring the stock status of NVIDIA RTX 4090 GPUs.

    This cog periodically checks the stock status of NVIDIA RTX 4090 GPUs from a specified URL
    and notifies a Discord channel when the status changes.

    Attributes:
        token (str): Discord bot token.
        bot (commands.Bot): Discord bot instance.
        url (str): URL of the NVIDIA product API.
        session (Session): Session object for making HTTP requests.
        channel (discord.Channel): Discord channel where notifications are sent.
        last_status (bool): Last known availability status of the product.
    """
    def __init__(self, token, bot, url):
        """
        Initializes the RTXBot with given token and URL.

        Args:
            token (str): Discord bot token.
            bot (commands.Bot): Discord bot instance.
            url (str): URL to check the stock of NVIDIA RTX 4090.
        """
        self.token = token
        self.bot = bot
        self.url = url
        self.session = Session()
        self.channel = None
        self.last_status = False
        self.setup()

    def setup(self):
        """
        Sets up the bot commands, events, and session headers.
        This method is called during the initialization process.
        """
        # Set up User-Agent for session
        self.session.headers.update(
                {'User-Agent':
                 'Mozilla/5.0 (X11; Linux x86_64; rv:121.0) Gecko/20100101 Firefox/121.0'})

    @tasks.loop(minutes=2)
    async def check_stock_periodically(self):
        """
        A periodic task that checks the stock status of the NVIDIA RTX 4090 GPU every 2 minutes.

        If the stock status changes, it sends a notification message to the
        configured Discord channel.
        """
        if self.channel is None:
            print("Channel is none, exit check_stock_periodically")
            return

        await self.channel.send("Checking stock periodically from now...")

        product_info = await self.check_stock()

        if isinstance(product_info, str):
            print(product_info)
            return
        print(product_info, product_info.get('productAvailable'), self.last_status)
        if product_info and product_info.get('productAvailable') != self.last_status:
            self.last_status = "Available" if product_info.get('productAvailable') else "Out of Stock"
            product_title = product_info.get('productTitle', 'Unknown Product')
            product_price = product_info.get('productPrice', 'N/A')
            purchase_link = product_info.get('retailers', [{}])[0].get('purchaseLink', 'Not available')

            message = (f"**{product_title}** status changed!\n"
                       f"Status: {self.last_status}\n"
                       f"Price: {product_price}\n"
                       f"Link: {purchase_link}")
            await self.channel.send(message)

    @commands.command()
    async def hello(self, ctx):
        """
        An asynchronous command that sends a greeting message.

        When a user types '!hello' in a Discord channel, the bot responds with "Hello!".
        Args:
            ctx: The context under which the command is executed.
        """
        await ctx.send(f'Hello {ctx.author.mention}!')
        self.channel = ctx.channel
        if not self.check_stock_periodically.is_running():
            self.check_stock_periodically.start()

    @commands.Cog.listener()
    async def on_ready(self):
        """
        An asynchronous event that triggers when the bot is ready.

        Prints a message to the console indicating that the bot has successfully started.
        """
        print(f'{self.bot.user.name} started.')

    @commands.command()
    async def stock(self, ctx):
        """
        An asynchronous command that check the stock availability.

        Checks the stock availability of NVIDIA RTX 4090 FE.
        Sends the stock status, price, and purchase link.
        Args:
            ctx: The context under which the command is executed.
        """
        product_info = await self.check_stock()

        if isinstance(product_info, str):
            print(product_info)
            return
        if product_info:
            status = "Available" if product_info.get('productAvailable') else "Out of Stock"
            product_title = product_info.get('productTitle', 'Unknown Product')
            product_price = product_info.get('productPrice', 'N/A')
            purchase_link = product_info.get('retailers', [{}])[0].get('purchaseLink', 'Not available')

            message = (f"**{product_title}**\n"
                       f"Status: {status}\n"
                       f"Price: {product_price}\n"
                       f"Link: {purchase_link}")
            await ctx.send(message)
        else:
            await ctx.send("Product information is not available.")

    async def check_stock(self):
        """
        Checks the stock status of NVIDIA RTX 4090 from the NVIDIA API.

        Returns:
            dict or str: Product information if successful, error message otherwise.
        """
        try:
            response = self.session.get(self.url, timeout=10)
            if response.status_code == 200:
                data = json.loads(response.text)
                featured_product = data.get("searchedProducts", {}).get("featuredProduct")
                return featured_product
            return "Failed to retrieve information from NVIDIA API."
        except RequestException as exc:
            return f"Error during NVIDIA API request: {exc}"
