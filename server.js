const express = require("express");
const mongoose = require("mongoose");
const bodyParser = require("body-parser");
const cors = require("cors");

const app = express();

// Middleware
app.use(bodyParser.json());
app.use(cors());

// Connect to MongoDB
mongoose
  .connect("mongodb://localhost:27017/Med_Voice", { useNewUrlParser: true, useUnifiedTopology: true })
  .then(() => console.log("Connected to MongoDB"))
  .catch((error) => console.error("MongoDB connection error:", error));

// Define the Patient Schema
const patientSchema = new mongoose.Schema({
  name: String,
  age: Number,
  gender: String,
  symptoms: String, // Comma-separated string of symptoms
  prescribed_medications: String, // Prescribed medications (could be a comma-separated string as well)
});

// Create the Patient model
const Patient = mongoose.model("Patient", patientSchema);

// POST route to save patient data
app.post("/api/patient", async (req, res) => {
  const { name, age, gender, symptoms, prescribed_medications } = req.body;

  try {
    const newPatient = new Patient({
      name,
      age,
      gender,
      symptoms,
      prescribed_medications,
    });

    const savedPatient = await newPatient.save();
    res.status(201).json(savedPatient);
  } catch (error) {
    console.error("Error saving patient data:", error);
    res.status(500).send("Error saving patient data.");
  }
});

// Start the server
const PORT = 8080;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
