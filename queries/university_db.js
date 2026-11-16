// CRUD practice in mongosh against a MongoDB Atlas cluster.
// Run with: mongosh "<connection-string>" --username <user> --file queries/university_db.js

db = db.getSiblingDB("UniversityDB");
db.students.drop();
db.createCollection("students");

// Create
db.students.insertOne({ studentID: 101, name: "Alice", major: "Computer Science", age: 21, gpa: 3.8 });
db.students.insertMany([
  { studentID: 102, name: "Bob", major: "Data Science", age: 22, gpa: 3.5 },
  { studentID: 103, name: "Charlie", major: "Computer Science", age: 20, gpa: 3.9 },
  { studentID: 104, name: "Diana", major: "Cybersecurity", age: 23, gpa: 3.6 },
  { studentID: 105, name: "Emma", major: "Data Science", age: 21, gpa: 3.7 }
]);

// Read
printjson(db.students.find({ major: "Computer Science" }).toArray());
printjson(db.students.find({ gpa: { $gte: 3.7 } }).toArray());
printjson(db.students.find({}, { _id: 0, name: 1, major: 1 }).toArray());
printjson(db.students.find().sort({ gpa: -1 }).toArray());

// Update
db.students.updateOne({ studentID: 101 }, { $set: { gpa: 3.95 } });
db.students.updateOne({ studentID: 102 }, { $set: { graduationYear: 2027 } });
db.students.updateOne({ name: "Charlie" }, { $set: { major: "Software Engineering" } });

// Delete
db.students.deleteOne({ studentID: 105 });

// Results
printjson(db.students.find({ gpa: { $gt: 3.6 } }).toArray());
printjson(db.students.find().sort({ age: 1 }).toArray());
print("Total students:", db.students.countDocuments());
