from src.models.patched_deepseek import PatchedChatDeepSeek


def main():
    model = PatchedChatDeepSeek(model_name="deepseek-v4-flash", api_key="sk-2497ca6339ee4ae586e1ee76c6b92535")
    response = model.invoke("What is the weather in Tokyo?")
    print(response.content)


if __name__ == "__main__":
    main()
