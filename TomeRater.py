###################### TO DO ############################
# This is an unfinished version - enough to do what it
# needs to, but there's plenty of room for some additions
# that would improve it.
#
# 1) Better end-to-end error handling
# 2) UI approach, with prompts and menu's
# 3) Ability to manage additions (like TLD's) on the fly
# 4) Fixing the return of <> object notes
########################################################

# Start by constructing the User class:
class User(object):
    
    ############ START DUNDER METHODS ############
    def __init__(self, name, email):
        # the users name
        self.name = name
        # their email address
        self.email = email
        # we want to capture how many books the user has read, so we'll start by creating
        # a blank dictionary to store these in later.
        self.books = {}
    
    def __repr__(self):
        # before we return the message, we want to check if it's "book" should be plural or not
        if len(self.books) == 1:
            book_s = "book"
        else:
            book_s = "books"
            
        # now we've got that, we'll return a meaningful message
        return("{user} ({email}) has read {book_count} {book_s}".format(user=self.name, email=self.email, book_count=len(self.books), book_s=book_s))
    
    def __eq__(self, user2):
        if self.name == user2.name and self.email == user2.email:
            # both pieces of data match, return True
            return True
        else:
            # at least one piece of data was different, so it's someone new - return False
            return False
    ############ END DUNDER METHODS ############
    
    ############ START OTHER METHODS ############
    def get_email(self):
        return self.email
    
    def change_email(self, new_email):
        # we want to grab the email that's currently in use for our response to the user once changed
        cur_email = self.email
        # We want to validate that the email address is valid.  Whilst we could use additional plugins
        # to validate at SMTP level, we will just record the TLD's that we are happy to accept
        valid_tlds = ['.com','.edu','.org']
        # We'll do a couple of checks at this point.
        if self.email == new_email:
            # the address they've provided is already assigned to the user
            return "The email address for {user} is already set to {email} - no changes made".format(user=self.user, email=self.email)
        elif new_email.count("@") != 1 or new_email[-4:] not in valid_tlds:
            # either, there wasn't an @ symbol, or the last four digits weren't in the valid TLD's
            return "The email address isn't in a valid format - no changes made"
        else:
            # there are other checks we could carry out, but for the purposes of this exercise, we'll halt here
            self.email = new_email
            return "The email address for {user} has been changed from {old} to {new}".format(user=self.user, old=cur_email, new=self.email)
        
    def read_book(self, book, rating=None):
        self.books[book] = rating
        
    def get_average_rating(self):
        return sum([bkrating for bkrating in self.books.values() if bkrating is not None]) / len(self.books)
    ############ END OTHER METHODS ############    
 
 
class Book(object):
    # As an additional check, we'll record the isbn's in a new list as we don't want to end up with
    # duplicate books/isbn's in the list.  Start with a blank list
    used_isbns = []
     
     
    ############ START DUNDER METHODS ############
    def __init__(self, title, isbn):
            # For a bit of a sanity check, we want to make sure that the user doesn't try to create a book
            # with the same ISBN as another book (as they should be unique).
            if isbn not in [used_isbn.isbn for used_isbn in self.__class__.used_isbns]:
                # it doesn't exist, so we can go ahead and create it
                # the title of the book
                self.title = title
                # the unique ISBN number
                self.isbn = isbn
                # List to hold on to the ratings (added through add_rating)
                self.ratings = []
                # add to the used_isbns list we created earlier
                self.__class__.used_isbns.append(self)
            else:
                print("Whoops! That ISBN is already in use, please check it and try again")
        
    def __eq__(self, book2):
        if self.title == book2.title and self.isbn == book2.isbn:
            # both pieces of data match, return True
            return True
        else:
            # at least one piece of data was different, so it's a new book - return False
            return False
    
    def __hash__(self):
        return hash((self.title, self.isbn))

    ############ END DUNDER METHODS ############

    ############ START OTHER METHODS ############
        
    def get_title(self):
        return self.title
    
    def get_isbn(self):
        return self.isbn
    
    def set_isbn(self,new_isbn):
        # Start by capturing the original ISBN so we can use it in our confirmation message
        cur_isbn = self.isbn
        # Now we'll use the new ISBN that has been passed through to update the book
        self.isbn = new_isbn
        # Return the confirmation to the end user
        print("We've updated the ISBN of {book} from {cur_isbn} to {new_isbn}".format(book=self.title, cur_isbn=cur_isbn, new_isbn=self.isbn))
        
    def add_rating(self, rating):
        # We want to check that the rating is valid (0 - 4) so we'll do a quick check before adding
        if rating >= 0 and rating <= 4:
            # It's a valid rating, so let's add it
            self.ratings.append(rating)
        else:
            # It wasn't an acceptable rating - let the user know
            print("Whoops, " + self.rating + " isn't allowed, and must be between 0 and 4. Please check and try again.")
            # The exercise does suggest "Invalid Rating", but we want to use similar language throughout
            # our code... however, if it was a case of pass or fail - the above line could be commented
            # and the one below used instead.
            # print("Invalid Rating")
            
    def get_average_rating(self):
        return sum([bkrating for bkrating in self.ratings]) / len(self.ratings)
            
    ############ END OTHER METHODS ############    
    
class Fiction(Book):
    
    ############ START DUNDER METHODS ############
    def __init__(self, title, author, isbn):
        super().__init__(title, isbn)
        # The author of the book
        self.author = author
        
    def __repr__(self):
        return "{title} by {author}".format(title=self.title, author=self.author)
    
    ############ END DUNDER METHODS ############
    
    ############ START OTHER METHODS ############
    
    def get_author(self):
        return self.author
    
    ############ END OTHER METHODS ############

class Non_Fiction(Book):
    
    ############ START DUNDER METHODS ############
    def __init__(self, title, subject, level, isbn):
        super().__init__(title, isbn)
        # The title of the non-fiction piece
        self.title = title
        # The subject of the non-fiction piece
        self.subject = subject
        # The intended level of the non-fiction piece
        self.level = level
    
    def __repr__(self):
        # gramatically, we should make sure the tool uses the correct wording depending on the
        # situation - for example, using "a" or "an" in the correct way.  Ideally, we'd have it
        # so that we had all the "vowel sounding" starts, not just vowels, but for the course of
        # this - we'll just use the first letter rule.
        vowels = ['a','e','i','o','u']
        if self.level[0].lower() in vowels:
            a_an = "an"
        else:
            a_an = "a"
        
        # Now that we've picked whether to use "a" or "an", we'll return the message
        return "{title}, {a_an} {level} manual on {subject}".format(title=self.title, a_an=a_an, level=self.level, subject=self.subject)

    ############ END DUNDER METHODS ############
    
    ############ START OTHER METHODS ############
    
    def get_subject(self):
        return self.subject
    
    def get_level(self):
        return self.level

    ############ END OTHER METHODS ############
    
class TomeRater():

    ############ START DUNDER METHODS ############
    def __init__(self):
        # Create an empty dictionary that maps a users email to their user object
        self.users = {}
        # Create an empty dictionary that maps a book object to the number of users who read it
        self.books = {}
    ############ END DUNDER METHODS ############
    
    ############ START OTHER METHODS ############
    def create_book(self, title, isbn):
        return Book(title,isbn)
    
    def create_novel(self, title, author, isbn):
        return Fiction(title, author, isbn)
    
    def create_non_fiction(self, title, subject, level, isbn):
        return Non_Fiction(title, subject, level, isbn)
    
    def add_book_to_user(self, book, email, rating=None):
        # We want to double check that there is a user, rather than trying to assign a book to
        # a black hole - so we'll check in the dictionary (from the constructor) for their email
        if email in self.users:
            # the user exists, that's a good start - now we can move on
            self.users[email].read_book(book, rating)
            # check if a rating was supplied, if it was - add the rating
            if rating is not None:
                book.add_rating(rating)
            
            # check if the book is in the earlier created dictionary
            if book in self.books:
                # it exists, let's increment it by 1
                self.books[book] += 1
            else:
                # it doesn't exist, lets add it and set it to 1
                self.books[book] = 1
        else:
            # We have been unable to find the user, return an error to the user
            print("No user with email {email}!".format(email=email))
            
    def add_user(self, name, email, user_books=None):
        # Similar to our add_book_to_user method, we want to double check if the user already exists
        # but this time it's to make sure we don't duplicate the user.  As such, we'll ask our
        # question in reverse so that the error is always at the end
        if email not in self.users:
            # The user doesn't exist, that's a start.  We want to verify their email first though
            # as we're only allowing certain Top Level Domains (TLD) to be registered
            valid_tlds = ['.com','.edu','.org']
            if email.count("@") == 1 and email[-4:] in valid_tlds:
                new_user = User(name, email)
                # Add the user to the dictionary
                self.users[email] = new_user
                # If the user has already read some books at the time of creation, we'll add them
                if user_books is not None:
                    # They've got at least one book on their list - lets loop through and add
                    for book in user_books:
                        self.add_book_to_user(book, email)
            else:
                print("The email address for {name} isn't in a valid format - no changes made".format(name=name))
        else:
            print("Whoops, looks like that user already exists.")
            
    def print_catalog(self):
        #cat_count = self.books.count()
        #print("Printing {x} items in the catalog".format(x=cat_count))
        print("Fetching all books, please wait...\n")
        for book in self.books.keys():
            print(book)
            #print("\n")
        print("\nDone.")
        
    def print_users(self):
        print("Fetching all users, please wait...\n")
        for user in self.users.values():
            print(user)
        print("\nDone.")
        
    def most_read_book(self):
        return max(self.books, key=self.books.get)
    
    def highest_rated_book(self):
        # We'll start by grabbing the highest rating out of the averages
        highest_rating = max(rating.get_average_rating() for rating in self.books.keys())
        # then we'll match that up to the book before returning it to the user.  Note that it adds
        # on the square brackets - so we'll strip those off.
        return str([book for book in self.books.keys() if book.get_average_rating() == highest_rating]).strip("[").strip("]")
    
    def most_positive_user(self):
        # Similar to the "highest rated book", we start by grabbing the highest rated
        highest_rating = max(rating.get_average_rating() for rating in self.users.values())
        # then we'll match that up to the book before returning it to the user.  Note that it adds
        # on the square brackets - so we'll strip those off.
        return str([user for user in self.users.values() if user.get_average_rating() == highest_rating]).strip("[").strip("]")
    