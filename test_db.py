# Exercise 3.1: Date Display.
dd = input("Enter the day: ")
mm = input("Enter the month: ")
yy = input("Enter the year: ")
print(f"Today’s Date is : {dd}/{mm}/{yy}")

###########################################################

# Exercise 3.2: Positive, negative, odd, even check.
n = int(input("Enter a number: "))
if n > 0:
    if n % 2 == 0:
        print("The number is even and positive.")
    else:
        print("The number is odd and positive.")
elif n < 0:
    if n % 2 == 0:
        print("The number is even and negative.")
    else:
        print("The number is odd and negative")
else:
    print("The number is zero.")

###########################################################

# Exercise 3.3: Student score grading.
S = float(input("Enter your score: "))
if 0 <= S < 60:
    print("Grade: F")
elif 60 <= S <= 69:
    print("Grade: D")
elif 70 <= S <= 79:
    print("Grade: C")
elif 80 <= S <= 89:
    print("Grade: B")
elif 90 <= S <= 100:
    print("Grade: A")
else:
    print("Invalid score!")

###########################################################

# Exercise 3.4: Weather decision system.
raining = input("Is it raining?: ").strip().lower() == "true"
windy = input("Is it windy?: ").strip().lower() == "true"
temperature = float(input("What is the temperature?: "))

if raining:
    print("Stay indoors, it's raining.")
elif windy:
    if temperature > 20:
        print("Go for a walk, it's windy but warm.")
    else:
        print("Stay indoors, it's windy and cold.")
else:
    if temperature > 10:
        print("Go for a walk, the weather is fine.")
    else:
        print("Stay indoors, it's too cold.")

###########################################################

# Exercise 3.5: Count Vowels and Consonants in a string.
txt = str(input("Enter text: "))
txt = txt.lower().replace(" ", "")
vowel_count = 0
consonant_count = 0
vowels = "aeiou"
for char in txt:
    if char in vowels:
        vowel_count += 1
    else:
        consonant_count += 1
print("Number of vowels in text: ", vowel_count)
print("Number of consonants in text: ", consonant_count)

###########################################################

# Exercise 3.6: Reverse a String.
text = str(input("Enter text: "))
reverse_text = ""
for char in text :
    reverse_text = char + reverse_text
print(reverse_text)

###########################################################

# Exercise 3.7: Split a String.
text = "Life is not a bed of roses"

text1 = text[:7]
text2 = text[7:18]
text3 = text[18:]

print(text3 + text2 + text1)
print(text3 + text2+ text1)
