window.CareerLogic = (() => {
  const data = window.CAREER_DATA;
  const STATUSES = {
    APPROVED: "aprobada",
    REGULAR: "regular",
    NOT_REGULAR: "no_regularizada",
    NOT_TAKEN: "no_cursada",
  };

  const statusMap = Object.fromEntries(data.statusCatalog.map((status) => [status.id, status]));

  function cloneStatus(statuses = data.martinStatus) {
    return Object.fromEntries(data.subjects.map((subject) => [subject.id, statuses[subject.id] || STATUSES.NOT_TAKEN]));
  }

  function subjectName(id) {
    const subject = data.subjectsById[id];
    return subject ? subject.name : `Materia ${id}`;
  }

  function statusLabel(status) {
    return statusMap[status]?.label || status;
  }

  function satisfiesRegular(status) {
    return status === STATUSES.APPROVED || status === STATUSES.REGULAR;
  }

  function satisfiesApproved(status) {
    return status === STATUSES.APPROVED;
  }

  function requirementIsMissing(statuses, requirement) {
    const status = statuses[requirement.id] || STATUSES.NOT_TAKEN;
    return requirement.type === "regular" ? !satisfiesRegular(status) : !satisfiesApproved(status);
  }

  function getRequirements(subject) {
    return [
      ...subject.regularReq.map((id) => ({ id, type: "regular" })),
      ...subject.approvedReq.map((id) => ({ id, type: "aprobada" })),
    ];
  }

  function missingFor(subject, statuses) {
    return getRequirements(subject).filter((requirement) => requirementIsMissing(statuses, requirement));
  }

  function requirementLabel(requirement) {
    const action = requirement.type === "regular" ? "regularizar" : "aprobar final";
    return `${subjectName(requirement.id)}: falta ${action}`;
  }

  function describeRequirements(subject) {
    const regular = subject.regularReq.map(subjectName);
    const approved = subject.approvedReq.map(subjectName);
    const parts = [];

    if (regular.length) {
      parts.push(`Cursada regular: ${regular.join(", ")}`);
    }

    if (approved.length) {
      parts.push(`Final aprobado: ${approved.join(", ")}`);
    }

    return parts.length ? parts.join(" · ") : "Sin correlativas";
  }

  function describeMissing(missing) {
    return missing.length ? missing.map(requirementLabel).join("; ") : "Sin restricciones";
  }

  function evaluateSubject(subject, statuses) {
    const status = statuses[subject.id] || STATUSES.NOT_TAKEN;
    const missing = missingFor(subject, statuses);
    const needsCourse = status === STATUSES.NOT_TAKEN || status === STATUSES.NOT_REGULAR;

    return {
      subject,
      status,
      statusLabel: statusLabel(status),
      missing,
      eligible: needsCourse && missing.length === 0,
      blocked: needsCourse && missing.length > 0,
      finalPending: status === STATUSES.REGULAR,
      needsRecourse: status === STATUSES.NOT_REGULAR,
    };
  }

  function analyze(statusesInput) {
    const statuses = cloneStatus(statusesInput);
    const evaluations = data.subjects.map((subject) => evaluateSubject(subject, statuses));
    const byId = Object.fromEntries(evaluations.map((evaluation) => [evaluation.subject.id, evaluation]));
    const approved = evaluations.filter((evaluation) => evaluation.status === STATUSES.APPROVED);
    const regular = evaluations.filter((evaluation) => evaluation.status === STATUSES.REGULAR);
    const pendingFinals = evaluations.filter((evaluation) => evaluation.finalPending);
    const toRecourse = evaluations.filter((evaluation) => evaluation.needsRecourse);
    const eligible = evaluations.filter((evaluation) => evaluation.eligible);
    const blocked = evaluations.filter((evaluation) => evaluation.blocked);
    const secondLevel = evaluations.filter((evaluation) => evaluation.subject.level === 2);

    return {
      statuses,
      evaluations,
      byId,
      approved,
      regular,
      pendingFinals,
      toRecourse,
      eligible,
      blocked,
      secondLevel,
      secondEligible: secondLevel.filter((evaluation) => evaluation.eligible),
      secondBlocked: secondLevel.filter((evaluation) => evaluation.blocked),
      completionRate: approved.length / data.subjects.length,
    };
  }

  function directDependents(id) {
    return data.subjects
      .filter((subject) => getRequirements(subject).some((requirement) => requirement.id === Number(id)))
      .map((subject) => subject.id);
  }

  function transitiveDependents(id) {
    const visited = new Set();
    const queue = directDependents(id);

    while (queue.length) {
      const current = queue.shift();

      if (visited.has(current)) {
        continue;
      }

      visited.add(current);
      queue.push(...directDependents(current));
    }

    return [...visited].map((subjectId) => data.subjectsById[subjectId]);
  }

  function activeBlockingImpact(id, statusesInput) {
    const statuses = cloneStatus(statusesInput);
    const direct = data.subjects
      .filter((subject) => missingFor(subject, statuses).some((requirement) => requirement.id === Number(id)))
      .map((subject) => data.subjectsById[subject.id]);
    const transitive = transitiveDependents(id);
    const combined = [...new Map([...direct, ...transitive].map((subject) => [subject.id, subject])).values()];

    return {
      direct,
      transitive,
      combined,
      byLevel: [2, 3, 4, 5].map((level) => ({
        level,
        subjects: combined.filter((subject) => subject.level === level),
      })),
    };
  }

  function finalPriority(statusesInput) {
    const statuses = cloneStatus(statusesInput);
    const pendingFinals = data.subjects.filter((subject) => statuses[subject.id] === STATUSES.REGULAR);

    return pendingFinals
      .map((subject) => {
        const directApprovedBlocks = data.subjects.filter((candidate) =>
          candidate.approvedReq.includes(subject.id) &&
          missingFor(candidate, statuses).some((requirement) => requirement.id === subject.id && requirement.type === "aprobada")
        );
        const downstream = transitiveDependents(subject.id);
        const earlierDirect = directApprovedBlocks.filter((candidate) => candidate.level <= 3).length;
        const score = directApprovedBlocks.length * 4 + downstream.length + earlierDirect * 2;

        return {
          subject,
          score,
          directApprovedBlocks,
          downstream,
        };
      })
      .sort((a, b) => b.score - a.score || a.subject.id - b.subject.id);
  }

  function listNames(evaluations) {
    return evaluations.map((evaluation) => evaluation.subject.name).join(", ");
  }

  function makeAlternatives(statusesInput) {
    const analysis = analyze(statusesInput);
    const secondNames = listNames(analysis.secondEligible) || "ninguna materia nueva de segundo nivel";
    const recourseNames = analysis.toRecourse.map((evaluation) => evaluation.subject.name).join(", ") || "ningun recursado";
    const priority = finalPriority(statusesInput);
    const priorityName = priority[0]?.subject.name || "el final pendiente con mas impacto";
    const blockedCore = [13, 14, 16]
      .map((id) => analysis.byId[id])
      .filter((evaluation) => evaluation?.blocked)
      .map((evaluation) => evaluation.subject.name);

    return [
      {
        id: "advance",
        title: "Alternativa 1 - Avanzar todo lo posible",
        focus: "Cursar las materias habilitadas de segundo nivel y no perder ritmo academico.",
        actions: [
          `Inscribirse en: ${secondNames}.`,
          `Mantener en agenda el recursado de: ${recourseNames}.`,
          `Preparar al menos un final pendiente, con prioridad inicial en ${priorityName}.`,
        ],
        advantage: "Permite sumar regularidades nuevas rapidamente y conservar motivacion.",
        risk: blockedCore.length
          ? `No resuelve de inmediato el bloqueo del nucleo de programacion: ${blockedCore.join(", ")}.`
          : "Puede aumentar la carga si se intenta cursar todo al mismo tiempo.",
      },
      {
        id: "unlock",
        title: "Alternativa 2 - Destrabar correlatividades",
        focus: "Atacar primero las materias que generan mayor efecto en cadena.",
        actions: [
          `Recursar ${recourseNames} como prioridad operativa.`,
          `Rendir ${priorityName} en la primera mesa conveniente.`,
          "Cursar una seleccion acotada de materias habilitadas para no saturar el calendario.",
        ],
        advantage: "Reduce el riesgo de arrastrar bloqueos hacia tercer y cuarto nivel.",
        risk: "El avance visible en cantidad de materias nuevas puede ser menor durante el proximo periodo.",
      },
      {
        id: "balanced",
        title: "Alternativa 3 - Planificacion equilibrada",
        focus: "Combinar avance, recursado y finales con una carga sostenible.",
        actions: [
          `Recursar ${recourseNames}.`,
          `Cursar materias habilitadas de buena relacion esfuerzo/impacto: ${secondNames}.`,
          `Preparar ${priorityName}; dejar el segundo final como objetivo posterior si la carga lo permite.`,
        ],
        advantage: "Sostiene progreso sin ignorar las correlatividades criticas.",
        risk: "Exige seguimiento semanal para que el recursado y el final no queden relegados.",
        recommended: true,
      },
    ];
  }

  function buildReport(statusesInput) {
    const analysis = analyze(statusesInput);
    const priority = finalPriority(statusesInput);
    const algorithmsImpact = activeBlockingImpact(6, statusesInput);
    const mathImpact = activeBlockingImpact(1, statusesInput);
    const physicsImpact = activeBlockingImpact(3, statusesInput);
    const alternatives = makeAlternatives(statusesInput);
    const recommended = alternatives.find((alternative) => alternative.recommended) || alternatives[0];

    return {
      situation: "Martin finalizo primer nivel con Algoritmos y Estructuras de Datos no regularizada, Analisis Matematico I regular, Fisica I regular y el resto de primer nivel aprobado.",
      restrictions: analysis.secondBlocked.map((evaluation) => ({
        name: evaluation.subject.name,
        reason: describeMissing(evaluation.missing),
      })),
      alternatives,
      recommendation: recommended,
      answers: [
        {
          question: "1. Que asignaturas de segundo nivel puede cursar",
          answer: listNames(analysis.secondEligible) || "No tiene asignaturas de segundo nivel habilitadas.",
        },
        {
          question: "2. Que asignaturas no puede cursar y por que",
          answer: analysis.secondBlocked.length
            ? analysis.secondBlocked.map((evaluation) => `${evaluation.subject.name}: ${describeMissing(evaluation.missing)}`).join(" | ")
            : "No hay materias de segundo nivel bloqueadas con el estado actual.",
        },
        {
          question: "3. Consecuencias de no haber regularizado Algoritmos y Estructuras de Datos",
          answer: `Bloquea directamente ${algorithmsImpact.direct.map((subject) => subject.name).join(", ")}. Si se posterga, tambien compromete materias posteriores como ${algorithmsImpact.combined
            .filter((subject) => subject.level >= 3)
            .slice(0, 8)
            .map((subject) => subject.name)
            .join(", ")}.`,
        },
        {
          question: "4. Final a priorizar entre Analisis Matematico I y Fisica I",
          answer: priority[0]
            ? `Conviene priorizar ${priority[0].subject.name}, porque destraba mas requisitos de final aprobado y tiene mas impacto temprano en la cadena academica. Fisica I tambien importa, especialmente para Comunicacion de Datos, pero Analisis Matematico I afecta mas caminos posteriores.`
            : "No hay finales pendientes para comparar.",
        },
        {
          question: "5. Materias posteriores afectadas si posterga estas asignaturas",
          answer: `Por Algoritmos: ${algorithmsImpact.combined.map((subject) => subject.name).join(", ")}. Por Analisis Matematico I: ${mathImpact.combined.map((subject) => subject.name).join(", ")}. Por Fisica I: ${physicsImpact.combined.map((subject) => subject.name).join(", ")}.`,
        },
        {
          question: "6. Planificacion posible para el proximo periodo academico",
          answer: `${recommended.title}: ${recommended.actions.join(" ")}`,
        },
        {
          question: "7. Alternativas razonables, ventajas y desventajas",
          answer: alternatives
            .map((alternative) => `${alternative.title}. Ventaja: ${alternative.advantage} Desventaja: ${alternative.risk}`)
            .join(" | "),
        },
      ],
    };
  }

  function reportAsText(statusesInput) {
    const report = buildReport(statusesInput);
    const lines = [
      "Actividad: Planifica tu carrera",
      "Resolucion del caso de Martin",
      "",
      "Situacion inicial",
      report.situation,
      "",
      "Restricciones",
      report.restrictions.length
        ? report.restrictions.map((item) => `- ${item.name}: ${item.reason}`).join("\n")
        : "- No hay restricciones activas.",
      "",
      "Alternativas",
      ...report.alternatives.flatMap((alternative) => [
        `- ${alternative.title}`,
        `  Foco: ${alternative.focus}`,
        `  Acciones: ${alternative.actions.join(" ")}`,
        `  Ventaja: ${alternative.advantage}`,
        `  Desventaja: ${alternative.risk}`,
      ]),
      "",
      "Recomendacion",
      `${report.recommendation.title}. ${report.recommendation.focus}`,
      "",
      "Preguntas de prueba",
      ...report.answers.map((item) => `${item.question}\n${item.answer}`),
      "",
      "Reflexion final",
      "Un sistema de informacion transforma datos academicos dispersos en informacion util cuando organiza estados, reglas y trayectorias posibles. En lugar de mirar solo materias aisladas, permite ver restricciones, impactos futuros y alternativas comparables para decidir con mejor fundamento.",
    ];

    return lines.join("\n");
  }

  return {
    STATUSES,
    statusMap,
    cloneStatus,
    statusLabel,
    subjectName,
    satisfiesRegular,
    satisfiesApproved,
    describeRequirements,
    describeMissing,
    evaluateSubject,
    analyze,
    directDependents,
    transitiveDependents,
    activeBlockingImpact,
    finalPriority,
    makeAlternatives,
    buildReport,
    reportAsText,
  };
})();
