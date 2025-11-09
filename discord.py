import discord
from discord.ext import commands
import requests

# ------------------- CONFIGURACIÓN -------------------
# TODO: Reemplaza esto con tu información
TOKEN = "AQUÍ_TU_TOKEN_DEL_BOT"
API_URL = "http://IP_DE_TU_HOMELAB:5000" # Ej: "http://192.168.1.10:5000"
# ---------------------------------------------------

# Intents necesarios para escuchar mensajes y eventos
intents = discord.Intents.default()
intents.message_content = True  # Necesario para comandos con prefijo

bot = commands.Bot(command_prefix="!", intents=intents)

# --- INTERFAZ PRINCIPAL CON BOTONES ---
# timeout=None hace que esta vista sea persistente.
# ¡Los botones funcionarán incluso después de reiniciar el bot!
class ControlView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Encender Servidor", style=discord.ButtonStyle.green, custom_id="mc_start")
    async def start_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        # Mensaje de espera (diferido)
        await interaction.response.defer(ephemeral=True)
        
        try:
            response = requests.post(f"{API_URL}/encender-servidor")
            if response.status_code == 200:
                await interaction.followup.send("🟢 Servidor encendido correctamente.", ephemeral=True)
            else:
                await interaction.followup.send("⚠️ Error de la API al encender el servidor.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Error de conexión con la API: {str(e)}", ephemeral=True)

    @discord.ui.button(label="Apagar Servidor", style=discord.ButtonStyle.red, custom_id="mc_stop")
    async def stop_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        try:
            response = requests.post(f"{API_URL}/apagar-servidor")
            if response.status_code == 200:
                await interaction.followup.send("🔴 Servidor apagado correctamente.", ephemeral=True)
            else:
                await interaction.followup.send("⚠️ Error de la API al apagar el servidor.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Error de conexión con la API: {str(e)}", ephemeral=True)

    @discord.ui.button(label="Reiniciar Servidor", style=discord.ButtonStyle.gray, custom_id="mc_restart")
    async def restart_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        
        try:
            response = requests.post(f"{API_URL}/reiniciar-servidor")
            if response.status_code == 200:
                await interaction.followup.send("🔁 Servidor reiniciado correctamente.", ephemeral=True)
            else:
                await interaction.followup.send("⚠️ Error de la API al reiniciar el servidor.", ephemeral=True)
        except Exception as e:
            await interaction.followup.send(f"❌ Error de conexión con la API: {str(e)}", ephemeral=True)

# --- COMANDO PARA MOSTRAR LOS BOTONES ---
@bot.command()
@commands.has_permissions(administrator=True) # <-- ¡Importante!
async def panel(ctx):
    """Muestra el panel de control del servidor"""
    view = ControlView()
    await ctx.send("🎮 **Panel de Control del Servidor**", view=view)

# Manejador de errores para el comando 'panel'
@panel.error
async def panel_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("⛔ No tienes permiso para usar este comando.", ephemeral=True)
    else:
        await ctx.send(f"Ha ocurrido un error inesperado: {error}", ephemeral=True)

# --- EVENTO DE INICIO ---
@bot.event
async def on_ready():
    # Esto es necesario para que los botones persistentes se registren
    bot.add_view(ControlView())
    print(f"✅ Bot conectado como {bot.user}")
    print("Listo para recibir comandos.")

# Ejecuta el bot
try:
    bot.run(TOKEN)
except discord.errors.LoginFailure:
    print("❌ ERROR: El TOKEN del bot es incorrecto o no se ha proporcionado.")
except Exception as e:
    print(f"❌ Error al iniciar el bot: {e}")