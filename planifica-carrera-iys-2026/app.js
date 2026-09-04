(() => {
  const data = window.CAREER_DATA;
  const logic = window.CareerLogic;
  const STORAGE_KEY = "planifica-carrera-iys-2026";

  let statuses = loadStatuses();
  let selectedImpactId = 6;

  function $(selector) {
    return document.querySelector(selector);
  }

  function create(tag, className, text) {
    const element = document.createElement(tag);

    if (className) {
      element.className = className;
    }

    if (text !== undefined) {
      element.textContent = text;
    }

    return element;
  }

  function loadStatuses() {
    try {
      const saved = JSON.parse(localStorage.getItem(STORAGE_KEY));
      return logic.cloneStatus(saved || data.martinStatus);
    } catch {
      return logic.cloneStatus(data.martinStatus);
    }
  }

  function saveStatuses() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(statuses));
  }

  function groupedByLevel(items) {
    return [1, 2, 3, 4, 5].map((level) => ({
      level,
      items: items.filter((item) => item.subject.level === level),
    }));
  }

  function render() {
    const analysis = logic.analyze(statuses);

    renderMetrics(analysis);
    renderEditor(analysis);
    renderPlan(analysis);
    renderSecondLevel(analysis);
    renderImpact(analysis);
    renderAlternatives();
    renderReport();
    renderSources();
  }

  function renderMetrics(analysis) {
    const metrics = [
      { label: "Avance", value: `${analysis.approved.length}/${data.subjects.length}`, detail: `${Math.round(analysis.completionRate * 100)}% aprobado` },
      { label: "Cursables ahora", value: analysis.secondEligible.length, detail: "segundo nivel" },
      { label: "Bloqueadas", value: analysis.secondBlocked.length, detail: "segundo nivel" },
      { label: "Finales pendientes", value: analysis.pendingFinals.length, detail: analysis.pendingFinals.map((item) => item.subject.name).join(", ") || "sin pendientes" },
      { label: "Recursar", value: analysis.toRecourse.length, detail: analysis.toRecourse.map((item) => item.subject.name).join(", ") || "sin recursado" },
    ];

    const container = $("#metrics");
    container.replaceChildren();

    for (const metric of metrics) {
      const card = create("article", "metric");
      card.append(create("span", "metric-label", metric.label));
      card.append(create("strong", "metric-value", String(metric.value)));
      card.append(create("span", "metric-detail", metric.detail));
      container.append(card);
    }
  }

  function renderEditor(analysis) {
    const container = $("#stateEditor");
    container.replaceChildren();

    for (const group of groupedByLevel(analysis.evaluations)) {
      const section = create("section", "level-editor");
      section.append(create("h3", "", `${group.level}° nivel`));

      const list = create("div", "editor-list");

      for (const evaluation of group.items) {
        const row = create("label", "editor-row");
        const title = create("span", "editor-title");
        title.append(create("span", "subject-code", evaluation.subject.code));
        title.append(create("span", "", evaluation.subject.name));

        const select = create("select", "status-select");
        select.setAttribute("aria-label", `Estado de ${evaluation.subject.name}`);
        select.dataset.subjectId = evaluation.subject.id;

        for (const status of data.statusCatalog) {
          const option = create("option", "", status.label);
          option.value = status.id;
          option.selected = evaluation.status === status.id;
          select.append(option);
        }

        row.append(title, select);
        list.append(row);
      }

      section.append(list);
      container.append(section);
    }

    container.querySelectorAll("select").forEach((select) => {
      select.addEventListener("change", (event) => {
        statuses[event.target.dataset.subjectId] = event.target.value;
        saveStatuses();
        render();
      });
    });
  }

  function renderPlan(analysis) {
    const container = $("#planGrid");
    container.replaceChildren();

    for (const group of groupedByLevel(analysis.evaluations)) {
      const column = create("section", "plan-level");
      column.append(create("h3", "", `${group.level}° nivel`));

      for (const evaluation of group.items) {
        const tile = create("button", `subject-tile ${evaluation.status} ${evaluation.eligible ? "eligible" : ""} ${evaluation.blocked ? "blocked" : ""}`);
        tile.type = "button";
        tile.dataset.subjectId = evaluation.subject.id;
        tile.title = logic.describeRequirements(evaluation.subject);

        const top = create("span", "tile-top");
        top.append(create("span", "subject-code", evaluation.subject.code));
        top.append(create("span", "period", evaluation.subject.period));

        tile.append(top);
        tile.append(create("strong", "", evaluation.subject.name));
        tile.append(create("span", "tile-status", evaluation.eligible ? "Puede cursar" : evaluation.blocked ? "Bloqueada" : evaluation.statusLabel));

        tile.addEventListener("click", () => {
          selectedImpactId = evaluation.subject.id;
          renderImpact(analysis);
          $("#impact").scrollIntoView({ behavior: "smooth", block: "start" });
        });

        column.append(tile);
      }

      container.append(column);
    }
  }

  function renderSecondLevel(analysis) {
    const allowed = $("#secondAllowed");
    const blocked = $("#secondBlocked");
    allowed.replaceChildren();
    blocked.replaceChildren();

    for (const evaluation of analysis.secondEligible) {
      allowed.append(resultRow(evaluation.subject.name, logic.describeRequirements(evaluation.subject), "ok"));
    }

    if (!analysis.secondEligible.length) {
      allowed.append(emptyRow("No hay materias habilitadas."));
    }

    for (const evaluation of analysis.secondBlocked) {
      blocked.append(resultRow(evaluation.subject.name, logic.describeMissing(evaluation.missing), "danger"));
    }

    if (!analysis.secondBlocked.length) {
      blocked.append(emptyRow("No hay materias bloqueadas."));
    }
  }

  function resultRow(title, detail, tone) {
    const row = create("li", `result-row ${tone}`);
    row.append(create("strong", "", title));
    row.append(create("span", "", detail));
    return row;
  }

  function emptyRow(text) {
    const row = create("li", "result-row empty");
    row.append(create("span", "", text));
    return row;
  }

  function renderImpact() {
    const selector = $("#impactSubject");
    const report = logic.activeBlockingImpact(selectedImpactId, statuses);
    selector.replaceChildren();

    for (const subject of data.subjects) {
      const option = create("option", "", `${subject.code} - ${subject.name}`);
      option.value = subject.id;
      option.selected = subject.id === Number(selectedImpactId);
      selector.append(option);
    }

    const detail = $("#impactDetail");
    detail.replaceChildren();

    const selectedSubject = data.subjectsById[selectedImpactId];
    detail.append(create("h3", "", selectedSubject.name));

    if (!report.combined.length) {
      detail.append(create("p", "muted", "No se detectan materias posteriores dependientes."));
    } else {
      for (const group of report.byLevel.filter((item) => item.subjects.length)) {
        const block = create("div", "impact-level");
        block.append(create("strong", "", `${group.level}° nivel`));
        block.append(create("span", "", group.subjects.map((subject) => subject.name).join(", ")));
        detail.append(block);
      }
    }

    drawImpactCanvas(report);
  }

  function drawImpactCanvas(report) {
    const canvas = $("#impactCanvas");
    const ratio = window.devicePixelRatio || 1;
    const cssWidth = canvas.clientWidth || 640;
    const cssHeight = 230;
    canvas.width = cssWidth * ratio;
    canvas.height = cssHeight * ratio;
    canvas.style.height = `${cssHeight}px`;

    const context = canvas.getContext("2d");
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    context.clearRect(0, 0, cssWidth, cssHeight);

    const levels = [1, 2, 3, 4, 5];
    const margin = 38;
    const gap = (cssWidth - margin * 2) / (levels.length - 1);
    const selected = data.subjectsById[selectedImpactId];
    const affectedIds = new Set(report.combined.map((subject) => subject.id));

    context.lineWidth = 2;
    context.font = "12px system-ui, sans-serif";
    context.textAlign = "center";
    context.textBaseline = "middle";

    levels.forEach((level, index) => {
      const x = margin + index * gap;
      context.strokeStyle = "#d6ddd4";
      context.beginPath();
      context.moveTo(x, 45);
      context.lineTo(x, cssHeight - 34);
      context.stroke();
      context.fillStyle = "#56635d";
      context.fillText(`${level}°`, x, 22);
    });

    const nodes = [selected, ...report.combined].filter(Boolean);
    nodes.forEach((subject, index) => {
      const x = margin + (subject.level - 1) * gap;
      const y = 64 + ((index * 31) % 135);
      const isSelected = subject.id === Number(selectedImpactId);
      const affected = affectedIds.has(subject.id);

      context.beginPath();
      context.arc(x, y, isSelected ? 12 : 8, 0, Math.PI * 2);
      context.fillStyle = isSelected ? "#08766e" : affected ? "#d99b1f" : "#88938e";
      context.fill();
      context.strokeStyle = "#ffffff";
      context.lineWidth = 3;
      context.stroke();

      context.fillStyle = "#1f2825";
      context.textAlign = subject.level >= 4 ? "right" : "left";
      const labelX = subject.level >= 4 ? x - 14 : x + 14;
      context.fillText(subject.code, labelX, y);
    });

    context.strokeStyle = "#b7791f";
    context.lineWidth = 1.5;
    context.setLineDash([5, 5]);

    for (const subject of report.direct) {
      const startX = margin + (selected.level - 1) * gap;
      const endX = margin + (subject.level - 1) * gap;
      context.beginPath();
      context.moveTo(startX, cssHeight - 36);
      context.lineTo(endX, cssHeight - 36);
      context.stroke();
    }

    context.setLineDash([]);
  }

  function renderAlternatives() {
    const container = $("#alternatives");
    container.replaceChildren();

    for (const alternative of logic.makeAlternatives(statuses)) {
      const article = create("article", `alternative ${alternative.recommended ? "recommended" : ""}`);
      const header = create("header", "alternative-header");
      header.append(create("h3", "", alternative.title));

      if (alternative.recommended) {
        header.append(create("span", "badge ok", "Recomendada"));
      }

      article.append(header);
      article.append(create("p", "focus", alternative.focus));

      const actions = create("ul", "action-list");
      alternative.actions.forEach((action) => actions.append(create("li", "", action)));
      article.append(actions);

      const foot = create("div", "pros-cons");
      foot.append(create("p", "", `Ventaja: ${alternative.advantage}`));
      foot.append(create("p", "", `Desventaja: ${alternative.risk}`));
      article.append(foot);

      container.append(article);
    }
  }

  function renderReport() {
    const report = logic.buildReport(statuses);
    const container = $("#report");
    container.replaceChildren();

    const summary = create("section", "report-block");
    summary.append(create("h3", "", "Situacion inicial -> Restricciones -> Alternativas -> Recomendacion"));
    summary.append(create("p", "", report.situation));

    const restrictions = create("ul", "compact-list");
    if (report.restrictions.length) {
      report.restrictions.forEach((item) => restrictions.append(create("li", "", `${item.name}: ${item.reason}`)));
    } else {
      restrictions.append(create("li", "", "No hay restricciones activas."));
    }

    summary.append(restrictions);
    summary.append(create("p", "recommendation-line", `${report.recommendation.title}. ${report.recommendation.focus}`));
    container.append(summary);

    for (const item of report.answers) {
      const block = create("section", "report-block");
      block.append(create("h3", "", item.question));
      block.append(create("p", "", item.answer));
      container.append(block);
    }
  }

  function renderSources() {
    const container = $("#sources");
    container.replaceChildren();

    for (const source of data.sourceLinks) {
      const link = create("a", "", source.label);
      link.href = source.url;
      link.target = "_blank";
      link.rel = "noreferrer";
      container.append(link);
    }
  }

  function downloadReport() {
    const blob = new Blob([logic.reportAsText(statuses)], { type: "text/plain;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "resolucion-caso-martin.txt";
    link.click();
    URL.revokeObjectURL(url);
  }

  function setAllNotTaken() {
    statuses = logic.cloneStatus({});
    saveStatuses();
    render();
  }

  function resetMartin() {
    statuses = logic.cloneStatus(data.martinStatus);
    selectedImpactId = 6;
    saveStatuses();
    render();
  }

  $("#resetMartin").addEventListener("click", resetMartin);
  $("#clearScenario").addEventListener("click", setAllNotTaken);
  $("#downloadReport").addEventListener("click", downloadReport);
  $("#printReport").addEventListener("click", () => window.print());
  $("#impactSubject").addEventListener("change", (event) => {
    selectedImpactId = Number(event.target.value);
    renderImpact();
  });

  let resizeHandle = 0;
  window.addEventListener("resize", () => {
    clearTimeout(resizeHandle);
    resizeHandle = setTimeout(renderImpact, 120);
  });

  render();
})();
