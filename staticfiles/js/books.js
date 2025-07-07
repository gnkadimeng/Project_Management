// Book data storage
let books = [
{
 id: 1,
 title: "Advanced Web Development",
 status: "writing",
 author: "Sarah Johnson",
 dueDate: "2024-06-15",
 chapters: { 
     total: 15, 
     completed: 12,
     list: [
         { id: 1, number: 1, title: "Introduction to Web Development", author: "Sarah Johnson", editor: "John Smith", status: "Completed", lastUpdated: "2024-01-15" },
         { id: 2, number: 2, title: "HTML Fundamentals", author: "Sarah Johnson", editor: "John Smith", status: "Completed", lastUpdated: "2024-01-22" },
         { id: 3, number: 3, title: "CSS Styling", author: "Sarah Johnson", editor: "John Smith", status: "Completed", lastUpdated: "2024-02-05" }
     ]
 },
 description: "A comprehensive guide to modern web development techniques and best practices.",
 publisher: ""
},
{
 id: 2,
 title: "Modern JavaScript Patterns",
 status: "writing",
 author: "Michael Chen",
 dueDate: "2024-07-01",
 chapters: { 
     total: 10, 
     completed: 8,
     list: [
         { id: 1, number: 1, title: "JavaScript Basics", author: "Michael Chen", editor: "Lisa Wong", status: "Completed", lastUpdated: "2024-01-10" },
         { id: 2, number: 2, title: "Functions and Scope", author: "Michael Chen", editor: "Lisa Wong", status: "Completed", lastUpdated: "2024-01-18" }
     ]
 },
 description: "Exploring modern JavaScript patterns and best practices.",
 publisher: ""
},
{
 id: 3,
 title: "Data Science Handbook",
 status: "submission",
 author: "Emily Davis",
 dueDate: "",
 chapters: { 
     total: 12, 
     completed: 12,
     list: [
         { id: 1, number: 1, title: "Introduction to Data Science", author: "Emily Davis", editor: "Robert Taylor", status: "Completed", lastUpdated: "2023-11-15" },
         { id: 2, number: 2, title: "Data Cleaning Techniques", author: "Emily Davis", editor: "Robert Taylor", status: "Completed", lastUpdated: "2023-11-22" }
     ]
 },
 description: "A practical guide to data science techniques and applications.",
 publisher: "Tech Publications"
},
{
 id: 4,
 title: "Python for Beginners",
 status: "submission",
 author: "James Wilson",
 dueDate: "2024-05-30",
 chapters: { 
     total: 8, 
     completed: 8,
     list: [
         { id: 1, number: 1, title: "Getting Started with Python", author: "James Wilson", editor: "Maria Rodriguez", status: "Completed", lastUpdated: "2023-12-10" }
     ]
 },
 description: "An introduction to Python programming for complete beginners.",
 publisher: "Code Press"
}
];

// DOM Elements
const kanbanBoard = document.getElementById('kanbanBoard');
const tableView = document.getElementById('tableView');
const viewTabs = document.getElementById('viewTabs');
const searchInput = document.getElementById('searchInput');
const addNewBookBtn = document.getElementById('addNewBookBtn');
const saveBookBtn = document.getElementById('saveBookBtn');
const updateBookBtn = document.getElementById('updateBookBtn');
const bookForm = document.getElementById('bookForm');
const editBookForm = document.getElementById('editBookForm');
const chapterForm = document.getElementById('chapterForm');
const bookDetailsModal = new bootstrap.Modal(document.getElementById('bookDetailsModal'));
const addBookModal = new bootstrap.Modal(document.getElementById('addBookModal'));
const editBookModal = new bootstrap.Modal(document.getElementById('editBookModal'));
const chapterModal = new bootstrap.Modal(document.getElementById('chapterModal'));
const commentsModal = new bootstrap.Modal(document.getElementById('commentsModal'));
const confirmationModal = new bootstrap.Modal(document.getElementById('confirmationModal'));

// Current selected book for table view
let currentSelectedBook = null;

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
renderKanbanBoard();
setupEventListeners();
updateCounts();
});

// Set up event listeners
function setupEventListeners() {
// View switcher tabs
viewTabs.addEventListener('click', function(e) {
 e.preventDefault();
 if (e.target.tagName === 'A') {
     // Update active tab
     document.querySelectorAll('#viewTabs .nav-link').forEach(tab => {
         tab.classList.remove('active');
     });
     e.target.classList.add('active');
     
     // Show the selected view
     const view = e.target.dataset.view;
     if (view === 'kanban') {
         kanbanBoard.style.display = 'flex';
         tableView.style.display = 'none';
     } else {
         kanbanBoard.style.display = 'none';
         tableView.style.display = 'block';
         
         // If we have a selected book, show its chapters
         if (currentSelectedBook) {
             renderBookChapters(currentSelectedBook);
         }
     }
 }
});

// Search functionality
searchInput.addEventListener('input', function() {
 const searchTerm = this.value.toLowerCase();
 filterBooks(searchTerm);
});

// Add new book button
addNewBookBtn.addEventListener('click', function() {
 addBookModal.show();
});

// Save new book
saveBookBtn.addEventListener('click', function() {
 addNewBook();
});

// Update existing book
updateBookBtn.addEventListener('click', function() {
 updateBook();
});

// Add chapter button
document.getElementById('addChapterBtn').addEventListener('click', function() {
 if (!currentSelectedBook) return;
 
 // Reset form and set book ID
 chapterForm.reset();
 document.getElementById('chapterBookId').value = currentSelectedBook.id;
 document.getElementById('chapterId').value = '';
 document.getElementById('chapterModalTitle').textContent = 'Add New Chapter';
 
 // Set next chapter number
 const nextChapterNum = currentSelectedBook.chapters.list.length > 0 ? 
     Math.max(...currentSelectedBook.chapters.list.map(c => c.number)) + 1 : 1;
 document.getElementById('chapterNumber').value = nextChapterNum;
 
 chapterModal.show();
});

// Save chapter
document.getElementById('saveChapterBtn').addEventListener('click', function() {
 saveChapter();
});

// Print summary button
document.getElementById('printSummaryBtn').addEventListener('click', function() {
 window.print();
});

// Comment form submission
document.getElementById('commentForm').addEventListener('submit', function(e) {
 e.preventDefault();
 postComment();
});

// Setup drag and drop for kanban board
setupDragAndDrop();
}

// Render the kanban board with books
function renderKanbanBoard() {
// Clear all columns first
document.querySelectorAll('.kanban-column > div:first-child + div').forEach(column => {
 column.innerHTML = '';
});

// Add books to their respective columns
books.forEach(book => {
 addBookToKanban(book);
});
}

// Add a book to the kanban board
function addBookToKanban(book) {
const column = document.querySelector(`#${book.status}-column`);
if (!column) return;

const card = document.createElement('div');
card.className = 'kanban-card';
card.draggable = true;
card.dataset.id = book.id;

// Format due date
let dueDateText = '';
if (book.dueDate) {
 const dueDate = new Date(book.dueDate);
 dueDateText = `Due: ${dueDate.toLocaleDateString()}`;
}

// Calculate progress percentage
const progressPercent = Math.round((book.chapters.completed / book.chapters.total) * 100);

card.innerHTML = `
 <div class="kanban-card-header">
     <span class="kanban-card-title">${book.title}</span>
     <button class="btn btn-sm btn-outline-secondary" onclick="showBookDetails(${book.id})">
         <i class="bi bi-three-dots-vertical"></i>
     </button>
 </div>
 <div class="kanban-card-meta">
     <div>${book.author}</div>
     <div>${dueDateText}</div>
 </div>
 <div class="progress mb-2" style="height: 5px;">
     <div class="progress-bar bg-success" role="progressbar" style="width: ${progressPercent}%" 
         aria-valuenow="${progressPercent}" aria-valuemin="0" aria-valuemax="100"></div>
 </div>
 <div class="kanban-card-footer">
     <span>${book.chapters.completed}/${book.chapters.total} chapters</span>
     <div class="kanban-card-actions">
         <button class="btn btn-sm btn-outline-primary" title="Edit" onclick="editBook(${book.id}, event)">
             <i class="bi bi-pencil"></i>
         </button>
         <button class="btn btn-sm btn-outline-danger" title="Delete" onclick="confirmDeleteBook(${book.id}, event)">
             <i class="bi bi-trash"></i>
         </button>
     </div>
 </div>
`;

column.appendChild(card);
}

// Filter books based on search term
function filterBooks(searchTerm) {
if (!searchTerm) {
 renderKanbanBoard();
 return;
}

// Clear all columns first
document.querySelectorAll('.kanban-column > div:first-child + div').forEach(column => {
 column.innerHTML = '';
});

// Filter and display matching books
const filteredBooks = books.filter(book => 
 book.title.toLowerCase().includes(searchTerm) || 
 book.author.toLowerCase().includes(searchTerm) ||
 book.description.toLowerCase().includes(searchTerm)
);

filteredBooks.forEach(book => {
 addBookToKanban(book);
});

// Update counts for filtered books
updateCounts(filteredBooks);
}

// Update the count badges on each column
function updateCounts(filteredBooks = null) {
const booksToCount = filteredBooks || books;

const counts = {
 writing: 0,
 submission: 0,
 review: 0,
 production: 0,
 published: 0
};

booksToCount.forEach(book => {
 counts[book.status]++;
});

// Update the count badges
document.getElementById('writing-count').textContent = counts.writing;
document.getElementById('submission-count').textContent = counts.submission;
document.getElementById('review-count').textContent = counts.review;
document.getElementById('production-count').textContent = counts.production;
document.getElementById('published-count').textContent = counts.published;
}

// Add a new book
function addNewBook() {
if (!bookForm.checkValidity()) {
 bookForm.reportValidity();
 return;
}

const newBook = {
 id: books.length > 0 ? Math.max(...books.map(b => b.id)) + 1 : 1,
 title: document.getElementById('bookTitle').value,
 status: document.getElementById('initialStatus').value,
 author: document.getElementById('leadAuthor').value,
 dueDate: document.getElementById('dueDate').value,
 chapters: {
     total: parseInt(document.getElementById('totalChapters').value),
     completed: parseInt(document.getElementById('completedChapters').value),
     list: []
 },
 description: document.getElementById('bookDescription').value,
 publisher: document.getElementById('publisher').value
};

books.push(newBook);
addBookToKanban(newBook);
updateCounts();

// Reset form and close modal
bookForm.reset();
addBookModal.hide();
}

// Edit an existing book
function editBook(bookId, event) {
event.stopPropagation();

const book = books.find(b => b.id === bookId);
if (!book) return;

// Fill the edit form with book data
document.getElementById('editBookId').value = book.id;
document.getElementById('editBookTitle').value = book.title;
document.getElementById('editBookStatus').value = book.status;
document.getElementById('editLeadAuthor').value = book.author;
document.getElementById('editDueDate').value = book.dueDate || '';
document.getElementById('editBookDescription').value = book.description;
document.getElementById('editTotalChapters').value = book.chapters.total;
document.getElementById('editCompletedChapters').value = book.chapters.completed;
document.getElementById('editPublisher').value = book.publisher || '';

editBookModal.show();
}

// Update an existing book
function updateBook() {
if (!editBookForm.checkValidity()) {
 editBookForm.reportValidity();
 return;
}

const bookId = parseInt(document.getElementById('editBookId').value);
const bookIndex = books.findIndex(b => b.id === bookId);

if (bookIndex === -1) return;

// Update the book data
books[bookIndex] = {
 ...books[bookIndex],
 title: document.getElementById('editBookTitle').value,
 status: document.getElementById('editBookStatus').value,
 author: document.getElementById('editLeadAuthor').value,
 dueDate: document.getElementById('editDueDate').value || null,
 description: document.getElementById('editBookDescription').value,
 chapters: {
     ...books[bookIndex].chapters,
     total: parseInt(document.getElementById('editTotalChapters').value),
     completed: parseInt(document.getElementById('editCompletedChapters').value)
 },
 publisher: document.getElementById('editPublisher').value || ''
};

// Re-render the kanban board
renderKanbanBoard();
updateCounts();

// If this is the current selected book in table view, update that too
if (currentSelectedBook && currentSelectedBook.id === bookId) {
 currentSelectedBook = books[bookIndex];
 renderBookChapters(currentSelectedBook);
}

editBookModal.hide();
}

// Confirm deletion of a book
function confirmDeleteBook(bookId, event) {
event.stopPropagation();

const book = books.find(b => b.id === bookId);
if (!book) return;

// Set up the confirmation modal
document.getElementById('confirmationModalTitle').textContent = 'Delete Book';
document.getElementById('confirmationModalBody').innerHTML = `
 Are you sure you want to delete the book <strong>"${book.title}"</strong>? This action cannot be undone.
`;

// Set up the confirm button
const confirmBtn = document.getElementById('confirmActionBtn');
confirmBtn.onclick = function() {
 deleteBook(bookId);
 confirmationModal.hide();
};

confirmationModal.show();
}

// Delete a book
function deleteBook(bookId) {
books = books.filter(b => b.id !== bookId);

// Re-render the kanban board
renderKanbanBoard();
updateCounts();

// If this was the current selected book in table view, clear the table
if (currentSelectedBook && currentSelectedBook.id === bookId) {
 currentSelectedBook = null;
 document.getElementById('chaptersTableBody').innerHTML = `
     <tr>
         <td colspan="7" class="text-center text-muted py-4">
             No book selected. Please choose a book from the kanban view to see its chapters.
         </td>
     </tr>
 `;
}
}

// Show book details in modal
function showBookDetails(bookId) {
const book = books.find(b => b.id === bookId);
if (!book) return;

// Set this as the current selected book for table view
currentSelectedBook = book;

// Format dates
const createdDate = new Date().toLocaleDateString();
const dueDate = book.dueDate ? new Date(book.dueDate).toLocaleDateString() : 'Not set';

// Calculate progress
const progressPercent = Math.round((book.chapters.completed / book.chapters.total) * 100);

// Set modal title
document.getElementById('detailsModalTitle').textContent = book.title;

// Set modal content
document.getElementById('bookDetailsContent').innerHTML = `
 <div class="row mb-4">
     <div class="col-md-8">
         <p class="lead">${book.description}</p>
         <div class="row">
             <div class="col-md-6">
                 <h6>Lead Author</h6>
                 <p>${book.author}</p>
             </div>
             <div class="col-md-6">
                 <h6>Publisher</h6>
                 <p>${book.publisher || 'Not specified'}</p>
             </div>
         </div>
         <div class="row">
             <div class="col-md-6">
                 <h6>Created</h6>
                 <p>${createdDate}</p>
             </div>
             <div class="col-md-6">
                 <h6>Due Date</h6>
                 <p>${dueDate}</p>
             </div>
         </div>
     </div>
     <div class="col-md-4">
         <div class="card">
             <div class="card-body text-center">
                 <h5 class="card-title">Progress</h5>
                 <div class="progress mb-3" style="height: 20px;">
                     <div class="progress-bar bg-success" role="progressbar" style="width: ${progressPercent}%" 
                         aria-valuenow="${progressPercent}" aria-valuemin="0" aria-valuemax="100">${progressPercent}%</div>
                 </div>
                 <p class="card-text">${book.chapters.completed} of ${book.chapters.total} chapters completed</p>
             </div>
         </div>
     </div>
 </div>
 
 <h5 class="mb-3">Chapters</h5>
 <div class="table-responsive">
     <table class="table table-sm">
         <thead>
             <tr>
                 <th>#</th>
                 <th>Title</th>
                 <th>Author</th>
                 <th>Status</th>
                 <th>Last Updated</th>
             </tr>
         </thead>
         <tbody>
             ${generateChapterRows(book)}
         </tbody>
     </table>
 </div>
`;

// Set modal footer buttons
const modalFooter = document.querySelector('#bookDetailsModal .modal-footer');
modalFooter.innerHTML = `
 <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
 <button type="button" class="btn btn-primary" onclick="showTableView(${book.id})">
     <i class="bi bi-table"></i> View Full Chapters Table
 </button>
 <button type="button" class="btn btn-outline-primary" onclick="showComments(${book.id})">
     <i class="bi bi-chat-left-text"></i> Comments
 </button>
`;

bookDetailsModal.show();
}

// Show the table view for a specific book
function showTableView(bookId) {
const book = books.find(b => b.id === bookId);
if (!book) return;

// Switch to table view
document.querySelector('#viewTabs .nav-link[data-view="table"]').click();

// Set the book info in the table view header
document.getElementById('selectedBookTitle').textContent = book.title;
document.getElementById('selectedBookDescription').textContent = book.description;
document.getElementById('selectedBookAuthor').textContent = book.author;
document.getElementById('selectedBookDueDate').textContent = book.dueDate ? new Date(book.dueDate).toLocaleDateString() : 'Not set';

// Update progress bar
const progressPercent = Math.round((book.chapters.completed / book.chapters.total) * 100);
const progressBar = document.getElementById('selectedBookProgress');
progressBar.style.width = `${progressPercent}%`;
progressBar.setAttribute('aria-valuenow', progressPercent);
progressBar.textContent = `${progressPercent}%`;

// Enable the print button
document.getElementById('printSummaryBtn').disabled = false;

// Render the chapters table
renderBookChapters(book);

// Close the details modal
bookDetailsModal.hide();
}

// Render chapters for a book in the table view
function renderBookChapters(book) {
const tbody = document.getElementById('chaptersTableBody');

if (!book.chapters.list || book.chapters.list.length === 0) {
 tbody.innerHTML = `
     <tr>
         <td colspan="7" class="text-center text-muted py-4">
             No chapters found for this book.
         </td>
     </tr>
 `;
 return;
}

tbody.innerHTML = '';

book.chapters.list.forEach(chapter => {
 const statusClass = chapter.status.toLowerCase().replace(' ', '-');
 const row = document.createElement('tr');
 
 row.innerHTML = `
     <td>${chapter.number}</td>
     <td>${chapter.title}</td>
     <td>${chapter.author}</td>
     <td>${chapter.editor || '-'}</td>
     <td><span class="status-badge status-${statusClass}">${chapter.status}</span></td>
     <td>${new Date(chapter.lastUpdated).toLocaleDateString()}</td>
     <td>
         <button class="btn btn-sm btn-outline-primary" onclick="editChapter(${book.id}, ${chapter.id})">
             <i class="bi bi-pencil"></i>
         </button>
         <button class="btn btn-sm btn-outline-danger" onclick="confirmDeleteChapter(${book.id}, ${chapter.id})">
             <i class="bi bi-trash"></i>
         </button>
     </td>
 `;
 
 tbody.appendChild(row);
});
}

// Edit a chapter
function editChapter(bookId, chapterId) {
const book = books.find(b => b.id === bookId);
if (!book) return;

const chapter = book.chapters.list.find(c => c.id === chapterId);
if (!chapter) return;

// Fill the chapter form
document.getElementById('chapterBookId').value = book.id;
document.getElementById('chapterId').value = chapter.id;
document.getElementById('chapterNumber').value = chapter.number;
document.getElementById('chapterTitle').value = chapter.title;
document.getElementById('chapterAuthor').value = chapter.author;
document.getElementById('chapterEditor').value = chapter.editor || '';
document.getElementById('chapterStatus').value = chapter.status;

// Update modal title
document.getElementById('chapterModalTitle').textContent = 'Edit Chapter';

chapterModal.show();
}

// Confirm deletion of a chapter
function confirmDeleteChapter(bookId, chapterId) {
const book = books.find(b => b.id === bookId);
if (!book) return;

const chapter = book.chapters.list.find(c => c.id === chapterId);
if (!chapter) return;

// Set up the confirmation modal
document.getElementById('confirmationModalTitle').textContent = 'Delete Chapter';
document.getElementById('confirmationModalBody').innerHTML = `
 Are you sure you want to delete chapter ${chapter.number}: <strong>"${chapter.title}"</strong>? This action cannot be undone.
`;

// Set up the confirm button
const confirmBtn = document.getElementById('confirmActionBtn');
confirmBtn.onclick = function() {
 deleteChapter(bookId, chapterId);
 confirmationModal.hide();
};

confirmationModal.show();
}

// Delete a chapter
function deleteChapter(bookId, chapterId) {
const bookIndex = books.findIndex(b => b.id === bookId);
if (bookIndex === -1) return;

// Remove the chapter
books[bookIndex].chapters.list = books[bookIndex].chapters.list.filter(c => c.id !== chapterId);

// Update completed chapters count if needed
const completedChapters = books[bookIndex].chapters.list.filter(c => c.status === 'Completed').length;
books[bookIndex].chapters.completed = completedChapters;

// Re-render the kanban board to update progress
renderKanbanBoard();

// If this is the current selected book in table view, update the table
if (currentSelectedBook && currentSelectedBook.id === bookId) {
 renderBookChapters(books[bookIndex]);
}
}

// Save a chapter (add new or update existing)
function saveChapter() {
if (!chapterForm.checkValidity()) {
 chapterForm.reportValidity();
 return;
}

const bookId = parseInt(document.getElementById('chapterBookId').value);
const chapterId = parseInt(document.getElementById('chapterId').value) || null;
const bookIndex = books.findIndex(b => b.id === bookId);

if (bookIndex === -1) return;

const chapterData = {
 id: chapterId || Date.now(), // Use existing ID or generate a new one
 number: parseInt(document.getElementById('chapterNumber').value),
 title: document.getElementById('chapterTitle').value,
 author: document.getElementById('chapterAuthor').value,
 editor: document.getElementById('chapterEditor').value || null,
 status: document.getElementById('chapterStatus').value,
 lastUpdated: new Date().toISOString().split('T')[0] // Today's date in YYYY-MM-DD format
};

if (chapterId) {
 // Update existing chapter
 const chapterIndex = books[bookIndex].chapters.list.findIndex(c => c.id === chapterId);
 if (chapterIndex !== -1) {
     books[bookIndex].chapters.list[chapterIndex] = chapterData;
 }
} else {
 // Add new chapter
 books[bookIndex].chapters.list.push(chapterData);
}

// Update completed chapters count
const completedChapters = books[bookIndex].chapters.list.filter(c => c.status === 'Completed').length;
books[bookIndex].chapters.completed = completedChapters;

// Re-render the kanban board to update progress
renderKanbanBoard();

// If this is the current selected book in table view, update the table
if (currentSelectedBook && currentSelectedBook.id === bookId) {
 renderBookChapters(books[bookIndex]);
}

chapterModal.hide();
}

// Show comments for a book
function showComments(bookId) {
const book = books.find(b => b.id === bookId);
if (!book) return;

// Set up the comments modal
document.getElementById('commentsModalLabel').textContent = `Comments for "${book.title}"`;

// In a real app, we would fetch comments from a server
// For this demo, we'll use some placeholder comments
const commentsContainer = document.getElementById('commentsContainer');
commentsContainer.innerHTML = `
 <div class="card mb-3">
     <div class="card-body">
         <div class="d-flex justify-content-between mb-2">
             <h6 class="card-title mb-0">John Smith</h6>
             <small class="text-muted">2 days ago</small>
         </div>
         <p class="card-text">Great progress on the first few chapters! The content is well-structured and easy to follow.</p>
     </div>
 </div>
 <div class="card">
     <div class="card-body">
         <div class="d-flex justify-content-between mb-2">
             <h6 class="card-title mb-0">Editor Team</h6>
             <small class="text-muted">1 week ago</small>
         </div>
         <p class="card-text">Please review chapter 3 for technical accuracy. We've noticed a few potential issues with the examples.</p>
     </div>
 </div>
`;

commentsModal.show();
}

// Post a new comment
function postComment() {
const commentText = document.getElementById('newComment').value.trim();
if (!commentText) return;

// In a real app, we would send this to a server
// For this demo, we'll just add it to the UI
const commentsContainer = document.getElementById('commentsContainer');
const newComment = document.createElement('div');
newComment.className = 'card mb-3';
newComment.innerHTML = `
 <div class="card-body">
     <div class="d-flex justify-content-between mb-2">
         <h6 class="card-title mb-0">You</h6>
         <small class="text-muted">Just now</small>
     </div>
     <p class="card-text">${commentText}</p>
 </div>
`;

commentsContainer.prepend(newComment);

// Clear the comment field
document.getElementById('newComment').value = '';
}

// Generate chapter rows for book details modal
function generateChapterRows(book) {
if (!book.chapters.list || book.chapters.list.length === 0) {
 return `
     <tr>
         <td colspan="5" class="text-center text-muted py-4">
             No chapters added yet.
         </td>
     </tr>
 `;
}

let rows = '';

book.chapters.list.forEach(chapter => {
 const statusClass = chapter.status.toLowerCase().replace(' ', '-');
 
 rows += `
     <tr>
         <td>${chapter.number}</td>
         <td>${chapter.title}</td>
         <td>${chapter.author}</td>
         <td><span class="status-badge status-${statusClass}">${chapter.status}</span></td>
         <td>${new Date(chapter.lastUpdated).toLocaleDateString()}</td>
     </tr>
 `;
});

return rows;
}

// Setup drag and drop functionality
function setupDragAndDrop() {
const columns = document.querySelectorAll('.kanban-column');

let draggedCard = null;

// Add event listeners to columns
columns.forEach(column => {
 column.addEventListener('dragover', dragOver);
 column.addEventListener('dragenter', dragEnter);
 column.addEventListener('dragleave', dragLeave);
 column.addEventListener('drop', drop);
});

// Add event listeners to cards (using event delegation since cards are dynamic)
document.addEventListener('dragstart', function(e) {
 if (e.target.classList.contains('kanban-card')) {
     draggedCard = e.target;
     setTimeout(() => {
         e.target.classList.add('dragging');
     }, 0);
 }
});

document.addEventListener('dragend', function(e) {
 if (e.target.classList.contains('kanban-card')) {
     e.target.classList.remove('dragging');
     draggedCard = null;
 }
});

function dragOver(e) {
 e.preventDefault();
}

function dragEnter(e) {
 e.preventDefault();
 this.classList.add('drop-zone');
}

function dragLeave() {
 this.classList.remove('drop-zone');
}

function drop() {
 this.classList.remove('drop-zone');
 
 if (draggedCard) {
     const newStatus = this.dataset.status;
     const bookId = parseInt(draggedCard.dataset.id);
     
     // Update the book's status in our data
     const book = books.find(b => b.id === bookId);
     if (book && book.status !== newStatus) {
         book.status = newStatus;
         updateCounts();
     }
     
     // Move the card to the new column
     const column = this.querySelector(`#${newStatus}-column`);
     if (column) {
         column.appendChild(draggedCard);
     }
 }
}
}

// Add book to kanban column when "Add Book" button is clicked in a column
document.querySelectorAll('.kanban-add-card').forEach(button => {
button.addEventListener('click', function() {
 const column = this.dataset.column;
 document.getElementById('initialStatus').value = column;
 addBookModal.show();
});
});

// Make functions available globally for HTML event handlers
window.showBookDetails = showBookDetails;
window.editBook = editBook;
window.confirmDeleteBook = confirmDeleteBook;
window.showTableView = showTableView;
window.showComments = showComments;
window.editChapter = editChapter;
window.confirmDeleteChapter = confirmDeleteChapter; 
 

 
 