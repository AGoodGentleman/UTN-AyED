window.CAREER_DATA = (() => {
  const statusCatalog = [
    {
      id: "aprobada",
      label: "Aprobada",
      short: "A",
      tone: "ok",
      description: "Final aprobado. Sirve como cursada y aprobada.",
    },
    {
      id: "regular",
      label: "Regular",
      short: "R",
      tone: "warn",
      description: "Cursada regularizada. Falta rendir final.",
    },
    {
      id: "no_regularizada",
      label: "No regularizada",
      short: "NR",
      tone: "danger",
      description: "Debe recursarse para contar como correlativa.",
    },
    {
      id: "no_cursada",
      label: "No cursada",
      short: "NC",
      tone: "idle",
      description: "Todavia no fue cursada.",
    },
  ];

  const subjects = [
    { id: 1, code: "01", level: 1, period: "1° semestre", name: "Analisis Matematico I", regularReq: [], approvedReq: [] },
    { id: 2, code: "02", level: 1, period: "1° semestre", name: "Algebra y Geometria Analitica", regularReq: [], approvedReq: [] },
    { id: 3, code: "03", level: 1, period: "2° semestre", name: "Fisica I", regularReq: [], approvedReq: [] },
    { id: 4, code: "04", level: 1, period: "2° semestre", name: "Ingles I", regularReq: [], approvedReq: [] },
    { id: 5, code: "05", level: 1, period: "1° semestre", name: "Logica y Estructuras Discretas", regularReq: [], approvedReq: [] },
    { id: 6, code: "06", level: 1, period: "2° semestre", name: "Algoritmos y Estructuras de Datos", regularReq: [], approvedReq: [] },
    { id: 7, code: "07", level: 1, period: "2° semestre", name: "Arquitectura de Computadoras", regularReq: [], approvedReq: [] },
    { id: 8, code: "08", level: 1, period: "2° semestre", name: "Sistemas y Procesos de Negocio", regularReq: [], approvedReq: [] },

    { id: 9, code: "09", level: 2, period: "1° semestre", name: "Analisis Matematico II", regularReq: [1, 2], approvedReq: [] },
    { id: 10, code: "10", level: 2, period: "2° semestre", name: "Fisica II", regularReq: [1, 3], approvedReq: [] },
    { id: 11, code: "11", level: 2, period: "1° semestre", name: "Ingenieria y Sociedad", regularReq: [], approvedReq: [] },
    { id: 12, code: "12", level: 2, period: "2° semestre", name: "Ingles II", regularReq: [4], approvedReq: [] },
    { id: 13, code: "13", level: 2, period: "1° semestre", name: "Sintaxis y Semantica de los Lenguajes", regularReq: [5, 6], approvedReq: [] },
    { id: 14, code: "14", level: 2, period: "2° semestre", name: "Paradigmas de Programacion", regularReq: [5, 6], approvedReq: [] },
    { id: 15, code: "15", level: 2, period: "2° semestre", name: "Sistemas Operativos", regularReq: [7], approvedReq: [] },
    { id: 16, code: "16", level: 2, period: "anual", name: "Analisis de Sistemas de Informacion", regularReq: [6, 8], approvedReq: [] },

    { id: 17, code: "17", level: 3, period: "1° semestre", name: "Probabilidad y Estadistica", regularReq: [1, 2], approvedReq: [] },
    { id: 18, code: "18", level: 3, period: "1° semestre", name: "Economia", regularReq: [], approvedReq: [1, 2] },
    { id: 19, code: "19", level: 3, period: "1° semestre", name: "Bases de Datos", regularReq: [13, 16], approvedReq: [5, 6] },
    { id: 20, code: "20", level: 3, period: "2° semestre", name: "Desarrollo de Software", regularReq: [14, 16], approvedReq: [5, 6] },
    { id: 21, code: "21", level: 3, period: "1° semestre", name: "Comunicacion de Datos", regularReq: [], approvedReq: [3, 7] },
    { id: 22, code: "22", level: 3, period: "2° semestre", name: "Analisis Numerico", regularReq: [9], approvedReq: [1, 2] },
    { id: 23, code: "23", level: 3, period: "anual", name: "Diseno de Sistemas de Informacion", regularReq: [14, 16], approvedReq: [4, 6, 8] },

    { id: 24, code: "24", level: 4, period: "1° semestre", name: "Legislacion", regularReq: [11], approvedReq: [] },
    { id: 25, code: "25", level: 4, period: "anual", name: "Ingenieria y Calidad de Software", regularReq: [19, 20, 23], approvedReq: [13, 14] },
    { id: 26, code: "26", level: 4, period: "2° semestre", name: "Redes de Datos", regularReq: [15, 21], approvedReq: [] },
    { id: 27, code: "27", level: 4, period: "1° semestre", name: "Investigacion Operativa", regularReq: [17, 22], approvedReq: [] },
    { id: 28, code: "28", level: 4, period: "1° semestre", name: "Simulacion", regularReq: [17], approvedReq: [9] },
    { id: 29, code: "29", level: 4, period: "2° semestre", name: "Tecnologias para la Automatizacion", regularReq: [10, 22], approvedReq: [9] },
    { id: 30, code: "30", level: 4, period: "anual", name: "Administracion de Sistemas de Informacion", regularReq: [18, 23], approvedReq: [16] },

    { id: 31, code: "31", level: 5, period: "2° semestre", name: "Inteligencia Artificial", regularReq: [28], approvedReq: [17, 22] },
    { id: 32, code: "32", level: 5, period: "2° semestre", name: "Ciencia de Datos", regularReq: [28], approvedReq: [17, 19] },
    { id: 33, code: "33", level: 5, period: "1° semestre", name: "Sistemas de Gestion", regularReq: [18, 27], approvedReq: [23] },
    { id: 34, code: "34", level: 5, period: "1° semestre", name: "Gestion Gerencial", regularReq: [24, 30], approvedReq: [18] },
    { id: 35, code: "35", level: 5, period: "1° semestre", name: "Seguridad en los Sistemas de Informacion", regularReq: [26, 30], approvedReq: [20, 21] },
    { id: 36, code: "36", level: 5, period: "anual", name: "Proyecto Final", regularReq: [25, 26, 30], approvedReq: [12, 20, 23] },
  ];

  const martinStatus = {
    1: "regular",
    2: "aprobada",
    3: "regular",
    4: "aprobada",
    5: "aprobada",
    6: "no_regularizada",
    7: "aprobada",
    8: "aprobada",
  };

  for (const subject of subjects) {
    if (!martinStatus[subject.id]) {
      martinStatus[subject.id] = "no_cursada";
    }
  }

  const sourceLinks = [
    {
      label: "UTN FRVT - Regimen de correlatividades ISI Plan 2023",
      url: "https://frvt.utn.edu.ar/correlatividades-ingenieria-en-sistemas-de-informacion/",
    },
    {
      label: "UTN FRM - Plan de estudio ISI Plan 2023",
      url: "https://www4.frm.utn.edu.ar/plan-de-estudio-ingenieria-en-sistemas-de-informacion/",
    },
  ];

  return {
    statusCatalog,
    subjects,
    subjectsById: Object.fromEntries(subjects.map((subject) => [subject.id, subject])),
    martinStatus,
    sourceLinks,
  };
})();
