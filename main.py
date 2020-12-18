from src.weather_bot import weather_bot


if __name__ == "__main__":
    weather_bot.polling(none_stop=True, interval=0)
