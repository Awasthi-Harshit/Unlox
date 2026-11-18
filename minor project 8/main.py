import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
# 1. Load API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise SystemExit("Error: API key not found. Check your .env file.")
# 2. Create prompt template
prompt = ChatPromptTemplate.from_template("""
You are a helpful vegetarian recipe assistant.
The user will tell you their ingredients or food preferences.
Suggest a suitable vegetarian recipe.
Include:
- Recipe name
- Preparation time and cooking time
- Ingredients with quantities
- Step-by-step instructions
- Optional tips
Keep the instructions simple and practical.
User request: {question}
""")
# 3. Get input from user
user_question = input("\nWhat would you like to cook? ")
if not user_question.strip():
    raise SystemExit("Please enter a recipe request.")
# 4. Initialize Gemini and generate recipe
try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.5-flash-lite",
        google_api_key=api_key
    )
    # Connect prompt template to Gemini
    chain = prompt | llm
    # Send user's question
    response = chain.invoke({
        "question": user_question
    })
    # 5. Display recipe
    content = response.content
    if isinstance(content, str):
        print(content)
    elif isinstance(content, list):
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                print(block.get("text", ""))
            elif isinstance(block, str):
                print(block)
    else:
        print(content)
except Exception as e:
    print("\nSomething went wrong:", e)
