const express = require('express');
const bodyParser = require('body-parser');
const mongoose = require('mongoose');
const cors = require('cors');

const app = express();

// Parse incoming request bodies in JSON format
app.use(bodyParser.json());

app.use(cors());
// Connect to the MongoDB database
//mongoose.connect('mongodb://localhost/annotations', {

mongoose.connect('mongodb://mongodb:27017/annotations', {
  useNewUrlParser: true,
  useUnifiedTopology: true
});



// Define a schema for annotations
const annotationSchema = new mongoose.Schema({
  "@context": String,
  "type": String,
  "content": String,
  "tags": [String],
  "created": Date,
  "modified": Date,
  "body": [mongoose.Schema.Types.Mixed],
  "id": String,
  "uri": String, 
  "creator": {
    "@type": String,
    "name": String,
    "email": String
  },
  "motivation": String,
  "target": { 
    "selector": [{
      "TextQuoteSelector": {
        "@type": String,
        "exact": String
      },
      "TextPositionSelector": {
        "@type": String,
        "start": Number,
        "end": Number
      }
    }]
  }
}, { strict: false });

// Create a model for annotations
const Annotation = mongoose.model('Annotation', annotationSchema);

const schema = Annotation.schema;
console.log(schema);

// API endpoint for creating a new annotation
app.post('/annotations', async (req, res) => {
  // Extract the relevant fields from the JSON-LD payload
  const {
    "@context": context,
    "id": _id,
    "type": type,
    "content": content,
    "body": body,
    "tags": tags,
    "created": created,
    "modified": modified,
    "creator": creator,
    "motivation": motivation,
    "target": target,
    "uri": uri,
  } = req.body;


  // Create a new annotation with the extracted fields
  const annotation = new Annotation({
    "@context": context,
    "id": _id,
    "type": type,
    "content": content,
    "body": body,
    "tags": tags,
    "created": created,
    "modified": modified,
    "creator": creator,
    "motivation": motivation,
    "target": target,
    "uri": uri,
  });

  try {
    // Save the annotation to the database
    await annotation.save();
    res.send(annotation);
  } catch (error) {
    res.status(400).send(error);
  }
});


// API endpoint for fetching all annotations
app.get('/annotations', async (req, res) => {
  try {
    const annotations = await Annotation.find({});
    res.send(annotations);
  } catch (error) {
    res.status(500).send(error);
    
  }
});

app.get('/annotationsquery', async (req, res) => {
    const uri = req.query.uri;
    try {
      const annotations = await Annotation.find({ uri: uri });
      res.send(annotations);
    } catch (error) {
      res.status(500).send(error);
    }
  });

// API endpoint for fetching a single annotation by ID
app.get('/annotations/:id', async (req, res) => {
  const id = req.params._id;
  try {
    const annotation = await Annotation.findById(id);
    if (annotation) {
      res.send(annotation);
    } else {
      res.status(404).send();
    }
  } catch (error) {
    res.status(403).send(error);
  }
});

// API endpoint for deleting an annotation by ID
app.delete('/annotations/:id', async (req, res) => {
    const id = req.params.id;
    try {
      const annotation = await Annotation.findByIdAndDelete(id);
      if (annotation) {
        res.send(annotation);
      } else {
        res.status(404).send();
      }
    } catch (error) {
      res.status(500).send(error);
    }
  });


  

// Start the server
const port = 3000;
app.listen(port, () => {
  console.log(`Annotation server listening on port ${port}`);
});
