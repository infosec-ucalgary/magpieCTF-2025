const express = require("express");
const cookieParser = require("cookie-parser");
var path = require("path");
const app = express();
const PORT = 3000;

// -- vigenere cipher --
// all the vigenere functions operate in lower case

/**
 * This function creates a cyclical key for vigenere encrypton.
 * @param {string} str The string to be encrypted.
 * @param {string} key The key of the cipher.
 * @returns A key of greater or equal length to str.
 */
function vigenere_key(str, key) {
  // generating a key to fit the length of str
  parts = [];
  for (let i = 0; i < Math.ceil(str.length / key.length); ++i) {
    parts.push(key.toLowerCase());
  }
  return parts.join("");
}

/**
 * Encrypts data using a vigenere cipher
 * @param {string} plaintext The text to be encrypted
 * @param {string} key The key to encrypt with
 * @returns A vigenere cipher encoded string.
 */
function vigenere_encrypt(plaintext, key) {
  let cipher_text = "";
  let _str = plaintext.toLowerCase();
  let _key = vigenere_key(_str, key);
  let _base = "a".charCodeAt(0);

  for (let i = 0; i < _str.length; i++) {
    // testing if not alpha
    if (/[a-z]/.test(_str[i]) === false) {
      cipher_text += _str[i];
      continue;
    }

    // converting in range 0-25
    let x =
      (_str[i].charCodeAt(0) - _base + (_key[i].charCodeAt(0) - _base)) % 26;

    // convert into alphabets(ASCII)
    cipher_text += String.fromCharCode(x + _base);
  }

  return cipher_text;
}

/**
 * Decrypts data using a vigenere cipher
 * @param {string} ciphertext The text to decrypt
 * @param {string} key The key to decrypt with
 * @returns A plaintext string.
 */
function vigenere_decrypt(ciphertext, key) {
  let orig_text = "";
  let _str = ciphertext.toLowerCase();
  let _key = vigenere_key(_str, key);
  let _base = "a".charCodeAt(0);

  for (let i = 0; i < _str.length; i++) {
    // converting in range 0-25
    let x =
      (_str[i].charCodeAt(0) - _base + (_key[i].charCodeAt(0) - _base)) % 26;

    // convert into alphabets(ASCII)
    orig_text += String.fromCharCode(x + _base);
  }
  return orig_text;
}

// -- server code --

// encryption related
const key = "jakewashere";
const user = "current-user";
const admin_user = "admin";
const guest_user = "guest";

app.use(express.static(path.join(__dirname, "public")));
app.use(cookieParser());

app.get("/", (req, res) => {
  // creating the cookie
  let _key = vigenere_encrypt(user, key);
  let _value = vigenere_encrypt(guest_user, key);

  // logging
  console.log(
    `Created cookie ${_key} = ${_value} for ${
      req.headers["x-forwarded-for"] || req.socket.remoteAddress
    }`
  );

  // setting the cookie
  res.cookie(_key, _value, {
    httpOnly: true,
    secure: true, // set to true if using HTTPS
    sameSite: "lax",
  });
  res.sendFile(path.join(__dirname, "public", "home.html"));
});

// adding routes
app.get("/login", (req, res) => {
  let _user = req.cookies[vigenere_encrypt(user, key)];
  res.status(200);

  // logging
  console.log(`Attempted login: cookies.user = ${_user}`);

  // testing
  if (_user === vigenere_encrypt(admin_user, key)) {
    // hacker cracked the cipher
    console.log(
      `Hacker cracked the cipher: cookies.${vigenere_encrypt(
        user,
        key
      )}(${user}) = ${vigenere_encrypt(admin_user, key)}(${admin_user})`
    );
    res.sendFile(path.join(__dirname, "public", "flag.html"));
  } else {
    // hacker failed or first visit
    res.sendFile(path.join(__dirname, "public", "hidden.html"));
  }
});

app.listen(PORT, (error) => {
  if (!error) console.log(`App running on port ${PORT}`);
  else console.log("Error on start:", error);
});
