#!/usr/bin/env node
/** Copy explore/ into public/ so Vercel serves HTML when output directory is public. */
import { cpSync, existsSync, rmSync } from "fs";

const src = "explore";
const dest = "public/explore";

if (!existsSync(src)) {
  console.error("explore/ not found");
  process.exit(1);
}

if (existsSync(dest)) rmSync(dest, { recursive: true, force: true });
cpSync(src, dest, { recursive: true });
console.log("Copied explore/ → public/explore/");
