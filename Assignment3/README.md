# CS4250-Web-Srch-Recommender-Systms

## Assignment 3: Inverted Index with MongoDB

Maintains a `documents` collection and an `inverted_index` collection in MongoDB as
documents are inserted, updated, and deleted. Each term stores a postings list of
`{docId, tf}` entries, and terms with no postings left are removed.

To run the program, make sure MongoDB is running ('brew services start mongodb-community@8.0'),
run 'pip install -r requirements.txt', then run 'python3 inverted_index.py'
