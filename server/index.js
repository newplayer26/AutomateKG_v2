const express = require("express");

const path = require("path");
const methodOverride = require("method-override");
const bodyParser = require("body-parser");
const ejsMate = require("ejs-mate");

require("dotenv").config({ path: path.join(__dirname, "..", ".env") });

const app = express();
const SSE = require("express-sse");
const sse = new SSE();
const morgan = require("morgan");
const { spawn } = require("child_process");

app.engine("ejs", ejsMate);
app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));

app.use(methodOverride("_method"));
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
);

app.use(morgan("dev"));
app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
  res.render("options");
});
app.get("/set_llm", (req, res) => {
  const { choice, token, model_name } = req.query;
  const python = spawn("python", [
    "../scripts/set_llm.py",
    choice,
    model_name,
    token,
  ]);
  const pythonPromise = new Promise((resolve, reject) => {
    python.stdout.on("data", (data) => {
      const output = data.toString();
      if (output.includes("LLM set to")) {
        resolve();
      }
      if (output.includes("Error setting LLM")) {
        reject;
      }
      console.log("out: ", data.toString());
    });

    python.stderr.on("data", (data) => {
      const output = data.toString();
      if (output.includes("LLM set to")) {
        resolve();
      }
      if (output.includes("Error setting LLM")) {
        reject;
      }
      console.log("err: ", data.toString());
    });
  });
  pythonPromise
    .then(() => {
      res.json({ success: true });
    })
    .catch(() => {
      res.json({ success: false });
    });
});

app.get("/analyze", (req, res) => {
  res.render("analyze");
});

app.post("/analyze", express.json({ limit: "10mb" }), (req, res) => {
  const { text } = req.body;
  const python = spawn("python", ["../scripts/analyze_text.py", text]);

  let uuid = "";
  let capturingID = false;

  const pythonPromise = new Promise((resolve, reject) => {
    python.stdout.on("data", (data) => {
      const lines = data.toString().split("\n");
      for (const line of lines) {
        if (capturingID) {
          console.log(line);
          resolve({ uuid: line.trim() });
        }
        if (line.trim() === "JSON output saved.") {
          capturingID = true;
          uuid = "";
        }
        // Ignore any other output
      }
    });

    python.on("close", (code) => {
      if (code !== 0) {
        reject({ error: `Analysis process exited with code ${code}` });
      }
    });
  });
  pythonPromise
    .then((result) => {
      console.log(result);
      res.json(result);
    })
    .catch((error) => {
      console.log(error);
      res.status(500).json(error);
    });
});

app.use((err, req, res, next) => {
  const { status = 500 } = err;
  if (!err.message) err.message = "Oops, something went wrong!";
  return res.status(status).render("error", { err });
});

if (process.env.NODE_ENV == "development") {
  // db.sequelize.sync({ force: true }).then((req) => {
  //   require("./seeders/seeds")();
  app.listen(process.env.PORT, () => {
    console.log(`Serving on ${process.env.PORT}`);
  });
  // });
} else if (process.env.NODE_ENV == "production") {
  //db.sequelize.sync().then((req) => {
  app.listen(process.env.PORT, () => {
    console.log(`Serving on ${process.env.PORT}`);
  });
  //});
}
