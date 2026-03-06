# name: Tim Groth
# date:
# description: Implementation of CRUD operations with DynamoDB — CS178 Lab 10
# proposed score: 0 (out of 5) -- if I don't change this, I agree to get 0 points.

import boto3

# boto3 uses the credentials configured via `aws configure` on EC2
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Books')

def create_book():
    print("Creating a Book")
    
    title = input("Enter book Title: ")
    pages = int(input("Enter number of Pages: "))
    
    table.put_item(
        Item={
            'Title': title,
            'Pages': pages
        }
    )

def print_all_books():
    """Scan the entire Books table and print each item."""
   
    # scan() retrieves ALL items in the table.
    # For large tables you'd use query() instead — but for our small
    # dataset, scan() is fine.
    response = table.scan()
    items = response.get("Items", [])
    
    if not items:
        print("No books found. Make sure your DynamoDB table has data.")
        return
    
    print(f"Found {len(items)} book(s):\n")
    for book in items:
        print_book(book)

def print_book(book):
    title = book.get("Title", "Unknown Title")
    pages = book.get("Pages", "Unknown Number of Pages")

    print(f"  Title  : {title}")
    print(f"  Pages   : {pages}")
    print()

def update_pages():
    title = input("What is the book title? ")
    try:
        pages = int(input("What is the page count (integer): "))
        table.update_item(
            Key={"Title": title},
            UpdateExpression="SET Pages = :p",
            ExpressionAttributeValues={":p": pages}
        )
        print("updating page count")
    except:
        print("error in updating book page count")

def delete_book():
    title = input("What is the book title? ")
    try:
        table.delete_item(
            Key={"Title": title}
        )
        print("deleting book")
    except:
        print("error in deleting book")


def query_book():
    title = input("What is the book title? ")
    response = table.get_item(Key={"Title": title})
    book = response.get("Item")
    if(book == None):
        print("book not found")
    else:
        try:
            print("The page count is : " + str(book["Pages"]))
        except:
            print("movie has no page count")


def print_menu():
    print("----------------------------")
    print("Press C: to CREATE a new book")
    print("Press R: to READ all books")
    print("Press U: to UPDATE a book's page count")
    print("Press D: to DELETE a book")
    print("Press Q: to QUERY a book's page count")
    print("Press X: to EXIT application")
    print("----------------------------")

def main():
    input_char = ""
    while input_char.upper() != "X":
        print_menu()
        input_char = input("Choice: ")
        if input_char.upper() == "C":
            create_book()
        elif input_char.upper() == "R":
            print_all_books()
        elif input_char.upper() == "U":
            update_pages()
        elif input_char.upper() == "D":
            delete_book()
        elif input_char.upper() == "Q":
            query_book()
        elif input_char.upper() == "X":
            print("exiting...")
        else:
            print("Not a valid option. Try again.")

main()
