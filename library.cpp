#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <memory>   // For smart pointers
#include <map>      // For fast lookups
#include <fstream>  // For File I/O
#include <sstream>  // For string parsing
#include <iomanip>

using namespace std;

// ==========================================
// 1. Abstract Base Class (Polymorphism)
// ==========================================
class LibraryItem {
protected:
    int id;
    string title;
    bool isBorrowed;

public:
    LibraryItem(int id, string title) : id(id), title(title), isBorrowed(false) {}
    
    virtual ~LibraryItem() {} // Virtual destructor is essential

    // Pure virtual function
    virtual void display() const = 0; 
    virtual string getType() const = 0;

    // Getters and Setters
    int getId() const { return id; }
    string getTitle() const { return title; }
    bool getStatus() const { return isBorrowed; }
    
    void setBorrowed(bool status) { isBorrowed = status; }

    // Serialization helper (for File I/O)
    virtual string toCSV() const {
        return to_string(id) + "," + title + "," + (isBorrowed ? "1" : "0");
    }
};

// ==========================================
// 2. Derived Classes
// ==========================================
class Book : public LibraryItem {
private:
    string author;
    int pages;

public:
    Book(int id, string title, string author, int pages) 
        : LibraryItem(id, title), author(author), pages(pages) {}

    void display() const override {
        cout << "[Book] ID: " << id << " | Title: " << setw(20) << left << title 
             << " | Author: " << setw(15) << left << author 
             << " | Status: " << (isBorrowed ? "Borrowed" : "Available") << endl;
    }

    string getType() const override { return "BOOK"; }

    string toCSV() const override {
        return "BOOK," + LibraryItem::toCSV() + "," + author + "," + to_string(pages);
    }
};

class Journal : public LibraryItem {
private:
    string publisher;
    int volume;

public:
    Journal(int id, string title, string publisher, int volume) 
        : LibraryItem(id, title), publisher(publisher), volume(volume) {}

    void display() const override {
        cout << "[Journal] ID: " << id << " | Title: " << setw(20) << left << title 
             << " | Publisher: " << setw(15) << left << publisher 
             << " | Vol: " << volume 
             << " | Status: " << (isBorrowed ? "Borrowed" : "Available") << endl;
    }

    string getType() const override { return "JOURNAL"; }

    string toCSV() const override {
        return "JOURNAL," + LibraryItem::toCSV() + "," + publisher + "," + to_string(volume);
    }
};

// ==========================================
// 3. Manager Class (STL & Logic)
// ==========================================
class LibraryManager {
private:
    // map<ID, ItemPointer> for O(log n) search efficiency
    map<int, unique_ptr<LibraryItem>> inventory;
    const string filename = "library_data.txt";

public:
    LibraryManager() {
        loadFromFile();
    }

    ~LibraryManager() {
        saveToFile();
    }

    void addItem(unique_ptr<LibraryItem> item) {
        if (inventory.find(item->getId()) != inventory.end()) {
            cout << "Error: ID already exists!\n";
            return;
        }
        inventory[item->getId()] = move(item);
        cout << "Item added successfully.\n";
    }

    void removeItem(int id) {
        auto it = inventory.find(id);
        if (it != inventory.end()) {
            inventory.erase(it);
            cout << "Item removed.\n";
        } else {
            cout << "Item not found.\n";
        }
    }

    void searchItem(string keyword) const {
        cout << "\n--- Search Results ---\n";
        bool found = false;
        // Using iterators to traverse the map
        for (const auto& pair : inventory) {
            // Check if title contains keyword (simple substring check)
            if (pair.second->getTitle().find(keyword) != string::npos) {
                pair.second->display();
                found = true;
            }
        }
        if (!found) cout << "No items found matching '" << keyword << "'.\n";
    }

    void toggleBorrow(int id) {
        auto it = inventory.find(id);
        if (it != inventory.end()) {
            bool currentStatus = it->second->getStatus();
            it->second->setBorrowed(!currentStatus);
            cout << "Item status updated to: " << (!currentStatus ? "Borrowed" : "Available") << endl;
        } else {
            cout << "Item not found.\n";
        }
    }

    void listAll() const {
        if (inventory.empty()) {
            cout << "Library is empty.\n";
            return;
        }
        cout << "\n--- Library Inventory ---\n";
        for (const auto& pair : inventory) {
            pair.second->display();
        }
        cout << "-------------------------\n";
    }

    // --- File I/O Logic ---
    void saveToFile() {
        ofstream outFile(filename);
        if (!outFile) {
            cerr << "Error saving data!\n";
            return;
        }
        for (const auto& pair : inventory) {
            outFile << pair.second->toCSV() << endl;
        }
        cout << "Data saved to " << filename << endl;
    }

    void loadFromFile() {
        ifstream inFile(filename);
        if (!inFile) return; // File might not exist on first run

        string line;
        while (getline(inFile, line)) {
            stringstream ss(line);
            string type, segment;
            vector<string> data;

            while (getline(ss, segment, ',')) {
                data.push_back(segment);
            }

            if (data.empty()) continue;

            // Factory Pattern logic for object creation
            if (data[0] == "BOOK") {
                // BOOK,id,title,isBorrowed,author,pages
                int id = stoi(data[1]);
                string title = data[2];
                bool borrowed = (data[3] == "1");
                string author = data[4];
                int pages = stoi(data[5]);

                auto book = make_unique<Book>(id, title, author, pages);
                book->setBorrowed(borrowed);
                inventory[id] = move(book);
            } 
            else if (data[0] == "JOURNAL") {
                // JOURNAL,id,title,isBorrowed,publisher,volume
                int id = stoi(data[1]);
                string title = data[2];
                bool borrowed = (data[3] == "1");
                string publisher = data[4];
                int volume = stoi(data[5]);

                auto journal = make_unique<Journal>(id, title, publisher, volume);
                journal->setBorrowed(borrowed);
                inventory[id] = move(journal);
            }
        }
        cout << "Data loaded from " << filename << endl;
    }
};

// ==========================================
// 4. Helper Functions
// ==========================================
void clearInput() {
    cin.clear();
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
}

// ==========================================
// 5. Main Execution
// ==========================================
int main() {
    LibraryManager lib;
    int choice;

    while (true) {
        cout << "\n=== Advanced Library System ===\n";
        cout << "1. Add Book\n2. Add Journal\n3. List All\n4. Search by Title\n5. Borrow/Return Item\n6. Remove Item\n7. Exit\n";
        cout << "Choice: ";
        
        if (!(cin >> choice)) {
            cout << "Invalid input.\n";
            clearInput();
            continue;
        }
        clearInput(); // Consume newline

        if (choice == 7) break;

        try {
            switch (choice) {
            case 1: {
                int id, pages;
                string title, author;
                cout << "Enter ID: "; cin >> id; clearInput();
                cout << "Enter Title: "; getline(cin, title);
                cout << "Enter Author: "; getline(cin, author);
                cout << "Enter Pages: "; cin >> pages;
                
                // Using make_unique (C++14 feature)
                lib.addItem(make_unique<Book>(id, title, author, pages));
                break;
            }
            case 2: {
                int id, vol;
                string title, pub;
                cout << "Enter ID: "; cin >> id; clearInput();
                cout << "Enter Title: "; getline(cin, title);
                cout << "Enter Publisher: "; getline(cin, pub);
                cout << "Enter Volume: "; cin >> vol;

                lib.addItem(make_unique<Journal>(id, title, pub, vol));
                break;
            }
            case 3:
                lib.listAll();
                break;
            case 4: {
                string keyword;
                cout << "Enter search keyword: "; getline(cin, keyword);
                lib.searchItem(keyword);
                break;
            }
            case 5: {
                int id;
                cout << "Enter ID to Borrow/Return: "; cin >> id;
                lib.toggleBorrow(id);
                break;
            }
            case 6: {
                int id;
                cout << "Enter ID to remove: "; cin >> id;
                lib.removeItem(id);
                break;
            }
            default:
                cout << "Unknown command.\n";
            }
        } catch (const exception& e) {
            cerr << "Exception occurred: " << e.what() << endl;
        }
    }
    return 0;
}