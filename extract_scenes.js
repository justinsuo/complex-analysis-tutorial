// Extract scene text + stable IDs from lessons.html for audio generation
const fs = require('fs');
const html = fs.readFileSync('lessons.html', 'utf8');

const m = html.match(/const LESSONS = (\[[\s\S]*?\n\];)/);
if (!m) { console.error('Could not find LESSONS array'); process.exit(1); }
const code = 'const LESSONS = ' + m[1] + '\nmodule.exports = LESSONS;';
const tmp = '/tmp/_lessons_extract.js';
fs.writeFileSync(tmp, code);
const LESSONS = require(tmp);

const scenes = [];
LESSONS.forEach((lesson, li) => {
  (lesson.scenes || []).forEach((s, si) => {
    scenes.push({ id: `L${li}_T${si}`, text: s.text, lesson: lesson.title, kind: 'teach' });
  });
  if (lesson.example) {
    if (lesson.example.intro) {
      scenes.push({ id: `L${li}_EI`, text: lesson.example.intro, lesson: lesson.title, kind: 'example_intro' });
    }
    (lesson.example.steps || []).forEach((s, si) => {
      scenes.push({ id: `L${li}_E${si}`, text: s.text, lesson: lesson.title, kind: 'example_step' });
    });
  }
});

fs.writeFileSync('scenes.json', JSON.stringify(scenes, null, 2));
console.log(`Extracted ${scenes.length} scenes from ${LESSONS.length} lessons.`);
