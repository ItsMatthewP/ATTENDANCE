import tkinter as tk
from tkinter import ttk
import openai
import threading
from mattAPIKey import OPENAI_API_KEY

# --- 1. SET YOUR API KEY HERE ---
# !! Never share this file with your key in it !!
API_KEY = {OPENAI_API_KEY}

# --- 2. Initialize the OpenAI Client ---
try:
    if API_KEY == "YOUR_API_KEY_HERE":
        # Don't initialize if the key hasn't been changed
        client = None
    else:
        client = openai.OpenAI(api_key=API_KEY)
except openai.OpenAIError as e:
    print(f"Failed to initialize OpenAI client: {e}")
    client = None

# --- 3. Function to handle the actual API call ---
def run_api_call(question):
    try:
        if not client:
            raise Exception("OpenAI API key is not set. Please add it to the script.")

        # --- This is the correct Python syntax for the API call ---
        response = client.chat.completions.create(
            model="gpt-4o",  # Using a valid, current model
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": question}
            ]
        )
        
        # Extract the answer text
        answer_text = response.choices[0].message.content

        # --- Update the GUI (must be done this way from a thread) ---
        answer_output.config(state="normal")
        answer_output.delete("1.0", tk.END)
        answer_output.insert(tk.END, answer_text.strip())
        answer_output.config(state="disabled")

    except Exception as e:
        # Show any errors in the output box
        answer_output.config(state="normal")
        answer_output.delete("1.0", tk.END)
        answer_output.insert(tk.END, f"Error: {e}")
        answer_output.config(state="disabled")
    
    finally:
        # Re-enable the submit button
        submit_button.config(state="normal")

# --- 4. Function to be called by the submit button ---
def handle_submit():
    question = question_entry.get()
    
    if question:
        submit_button.config(state="disabled")
        answer_output.config(state="normal")
        answer_output.delete("1.0", tk.END)
        answer_output.insert(tk.END, "Getting answer...")
        answer_output.config(state="disabled")
        
        # Start the API call in a new thread to avoid freezing
        threading.Thread(target=run_api_call, args=(question,)).start()

# --- Create the main application window ---
root = tk.Tk()
root.title("Python Q&A Client")
root.geometry("500x350")

main_frame = ttk.Frame(root, padding="10")
main_frame.pack(fill="both", expand=True)

# --- Input Box (Entry) ---
question_label = ttk.Label(main_frame, text="Enter your question:")
question_label.pack(pady=(0, 5), anchor="w")
question_entry = ttk.Entry(main_frame, width=60)
question_entry.pack(fill="x", expand=True)

# --- Submit Button ---
submit_button = ttk.Button(main_frame, text="Submit", command=handle_submit)
submit_button.pack(pady=10)

# --- Output Box (Text) ---
answer_label = ttk.Label(main_frame, text="Answer:")
answer_label.pack(pady=(5, 5), anchor="w")
answer_output = tk.Text(main_frame, height=10, width=60, state="disabled", wrap="word")
answer_output.pack(fill="both", expand=True)

# --- Start the GUI event loop ---
root.mainloop()