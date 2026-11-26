// generate.mjs — build the v4 poster end to end: run build_poster.py to
// emit poster.svg (a build artifact, never committed), then render it to
// entry.png at exactly 1024x1024 with the locally cached Chromium
// headless shell. Authoring tool only: the competition program
// (main.ts) never renders anything, it just delivers entry.png.
//
//   node generate.mjs
//
// No network: poster.svg is self-contained, no external references.

import { execFileSync } from 'node:child_process';
import { existsSync, readdirSync, renameSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

const here = fileURLToPath(new URL('.', import.meta.url));

// Step 1: emit poster.svg from the story data.
execFileSync('python3', [join(here, 'build_poster.py')],
             { cwd: here, stdio: 'inherit' });

const svgUrl = pathToFileURL(join(here, 'poster.svg')).href;
const shot = join(here, 'render.png');

function findChromium() {
  const cache = join(homedir(), '.cache', 'ms-playwright');
  for (const dir of readdirSync(cache).sort().reverse()) {
    if (!dir.startsWith('chromium_headless_shell')) continue;
    const bin = join(cache, dir, 'chrome-headless-shell-linux64',
                     'chrome-headless-shell');
    if (existsSync(bin)) return bin;
  }
  throw new Error('chromium headless shell not found under ' + cache);
}

execFileSync(findChromium(), [
  '--headless',
  '--disable-gpu',
  '--no-sandbox',
  '--hide-scrollbars',
  '--force-device-scale-factor=1',
  '--window-size=1024,1024',
  '--default-background-color=00000000',
  '--screenshot=' + shot,
  svgUrl,
], { stdio: 'inherit' });

renameSync(shot, join(here, 'entry.png'));
console.log('entry.png rendered from poster.svg');
