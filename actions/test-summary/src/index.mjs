// test-summary: see action.yml. tools/build-actions bundles this file into dist/index.js.
import * as core from '@actions/core';
import fs from 'node:fs';

async function main() {
  const title = core.getInput('title', { required: true });
  const pytestFile = core.getInput('pytest-output', { required: true });
  const smokeFile = core.getInput('smoke-output');

  // pytest -q ends with one line of counts: "9 passed in 0.05s", "1 failed, 8 passed in 0.07s".
  const lines = fs.existsSync(pytestFile) ? fs.readFileSync(pytestFile, 'utf8').trim().split('\n') : [];
  const result = lines.findLast((line) => / in [\d.]+s/.test(line)) || '';
  const counted = (word) => Number(result.match(new RegExp(`(\\d+) ${word}`))?.[1] || 0);
  const passed = counted('passed');
  const failed = counted('failed') + counted('error');
  if (!result) core.warning(`${pytestFile}: no pytest result line`);
  core.setOutput('passed', passed);
  core.setOutput('failed', failed);

  core.summary.addHeading(title, 3).addRaw(`pytest: ${result || 'no result'}`, true);
  if (smokeFile && fs.existsSync(smokeFile)) core.summary.addCodeBlock(fs.readFileSync(smokeFile, 'utf8').trim());
  core.info(`test-summary: ${title}: passed=${passed} failed=${failed}`);
  await core.summary.write();
}

main().catch((error) => core.setFailed(error.message));
