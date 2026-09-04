const fs = require("fs");
const path = require("path");
const vm = require("vm");
const assert = require("assert");

const context = {
  window: {},
  console,
};

vm.createContext(context);

for (const file of ["data.js", "logic.js"]) {
  const source = fs.readFileSync(path.join(__dirname, file), "utf8");
  vm.runInContext(source, context, { filename: file });
}

const data = context.window.CAREER_DATA;
const logic = context.window.CareerLogic;
const statuses = logic.cloneStatus(data.martinStatus);
const analysis = logic.analyze(statuses);

const secondAllowed = Array.from(analysis.secondEligible.map((item) => item.subject.id));
const secondBlocked = Array.from(analysis.secondBlocked.map((item) => item.subject.id));

assert.deepStrictEqual(secondAllowed, [9, 10, 11, 12, 15]);
assert.deepStrictEqual(secondBlocked, [13, 14, 16]);
assert.strictEqual(analysis.byId[13].missing[0].id, 6);
assert.strictEqual(analysis.byId[16].missing[0].id, 6);
assert.strictEqual(logic.finalPriority(statuses)[0].subject.id, 1);

const algorithmsImpact = logic.activeBlockingImpact(6, statuses);
assert(algorithmsImpact.direct.some((subject) => subject.id === 13));
assert(algorithmsImpact.combined.some((subject) => subject.id === 36));

console.log("OK - caso Martin calculado correctamente");
