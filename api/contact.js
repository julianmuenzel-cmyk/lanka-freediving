import { Resend } from "resend";

const RATE_WINDOW_MS = 60_000;
const RATE_MAX = 5;
const hits = new Map();

function rateLimit(ip) {
  const now = Date.now();
  const bucket = hits.get(ip) || [];
  const recent = bucket.filter((t) => now - t < RATE_WINDOW_MS);
  if (recent.length >= RATE_MAX) return false;
  recent.push(now);
  hits.set(ip, recent);
  return true;
}

function json(res, status, body) {
  res.statusCode = status;
  res.setHeader("Content-Type", "application/json");
  res.end(JSON.stringify(body));
}

export default async function handler(req, res) {
  if (req.method === "OPTIONS") {
    res.setHeader("Allow", "POST, OPTIONS");
    res.statusCode = 204;
    res.end();
    return;
  }

  if (req.method !== "POST") {
    json(res, 405, { error: "Method not allowed" });
    return;
  }

  const ip =
    (req.headers["x-forwarded-for"] || "").split(",")[0].trim() ||
    req.socket?.remoteAddress ||
    "unknown";

  if (!rateLimit(ip)) {
    json(res, 429, { error: "Too many requests. Try again in a minute." });
    return;
  }

  let body = req.body;
  if (typeof body === "string") {
    try {
      body = JSON.parse(body);
    } catch {
      json(res, 400, { error: "Invalid JSON" });
      return;
    }
  }
  if (!body || typeof body !== "object") {
    json(res, 400, { error: "Invalid request body" });
    return;
  }

  const { name, email, course, message, website } = body;

  if (website) {
    json(res, 200, { ok: true });
    return;
  }

  if (!name || !email || !course || !message) {
    json(res, 400, { error: "Please fill in all fields." });
    return;
  }

  const emailRe = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if (!emailRe.test(String(email).trim()) || String(name).trim().length < 2) {
    json(res, 400, { error: "Please check your name and email." });
    return;
  }

  if (String(message).trim().length < 10) {
    json(res, 400, { error: "Message is too short." });
    return;
  }

  const apiKey = process.env.RESEND_API_KEY;
  const to = process.env.CONTACT_TO_EMAIL || "hello@lankafreediving.com";
  const from =
    process.env.CONTACT_FROM_EMAIL || "Lanka Freediving <hello@lankafreediving.com>";

  if (!apiKey) {
    console.error("RESEND_API_KEY is not set");
    json(res, 503, { error: "Contact form is not configured yet." });
    return;
  }

  const subject = `[Lanka Freediving] ${course} — ${String(name).trim()}`;
  const text = [
    `Name: ${String(name).trim()}`,
    `Email: ${String(email).trim()}`,
    `Course: ${String(course).trim()}`,
    "",
    String(message).trim(),
  ].join("\n");

  const html = `
    <p><strong>Name:</strong> ${escapeHtml(String(name).trim())}</p>
    <p><strong>Email:</strong> ${escapeHtml(String(email).trim())}</p>
    <p><strong>Course:</strong> ${escapeHtml(String(course).trim())}</p>
    <hr>
    <p>${escapeHtml(String(message).trim()).replace(/\n/g, "<br>")}</p>
  `;

  try {
    const resend = new Resend(apiKey);
    const { error } = await resend.emails.send({
      from,
      to: [to],
      replyTo: String(email).trim(),
      subject,
      text,
      html,
    });

    if (error) {
      console.error("Resend error:", error);
      json(res, 502, { error: "Could not send message. Try WhatsApp instead." });
      return;
    }

    json(res, 200, { ok: true });
  } catch (err) {
    console.error("Contact send failed:", err);
    json(res, 502, { error: "Could not send message. Try WhatsApp instead." });
  }
}

function escapeHtml(s) {
  return s
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}
