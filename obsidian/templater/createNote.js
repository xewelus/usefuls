async function createNote (tp, dlgTitle) {
  try {
    return await createNoteInternal(tp, dlgTitle);
  }
  catch (e) {
    console.error(e);
    return {text: e.stack};
  }
}

async function createNoteInternal (tp, dlgTitle) {
    
  const MAX_CHARS = 60;

  let input = await tp.system.prompt(dlgTitle, null, false, true);
  if (input === null) return null;

  const leaf = app.workspace.getLeaf('tab'); 
  await leaf.openFile(tp.config.template_file);

  // if clipboard contains markdown link, then we need divide it to text and link
  let text = input
  let link = null
  const match = input.match(/^\[(.*)\]\((.*)\)$/)
  if (match !== null) {
    text = match[1]
    link = match[2]
    input = text + '\n' + link;
  }

  let i = input.indexOf('\n');

  let fileName = i === -1 ? input : input.substr(0, i);

  let alias = fileName;
  fileName = replaceInvalidChars(fileName);
    
  if (fileName.length > MAX_CHARS) fileName = fileName.substr(0, MAX_CHARS);

  let path = await getNewFilePath(app.vault, tp.date.now("YYYY/MM/DD/") + fileName);
  await tp.file.move(path);

  if (input === fileName) return {title: input, text: ''};

  alias = alias === fileName ? null : alias;

  if (alias !== null) {
      tp.hooks.on_all_templates_executed(async () => { 
        const file = tp.file.find_tfile(tp.file.path(true)); 
        await app.fileManager.processFrontMatter(file, (frontmatter) => { 
          frontmatter["alias"] = alias;
        }); 
      });
  }

  return {
    title: fileName,
    alias: alias,
    text: i === -1 ? '' : input.substr(i + 1)
  };
}

function replaceInvalidChars(fileName) {
  let s = fileName;
  while (true) {
    var prev = s;

    s = s.replace(":", " -").replace("*", "_").replace("\\", "_").replace("/", "_")
        .replace("<", "_").replace(">", "_").replace("|", "_").replace("?", "_")
        .replace("#", "_").replace("^", "_").replace("[", "(").replace("]", ")").replace("|", "I");
    
    if (s === prev) break;
  }

  if (s.length === 0) return "-";
  return s;
}

async function getNewFilePath(vault, relativeFilePath) {
    const i = relativeFilePath.lastIndexOf('/');
    const folderPath = relativeFilePath.substring(0, i);
    const baseFileName = relativeFilePath.substring(i + 1);

    let newFileName = baseFileName;
    let fileExists = await vault.adapter.exists(`${folderPath}/${newFileName}.md`);
    let counter = 1;

    while (fileExists) {
        newFileName = `${baseFileName} (${counter})`;
        fileExists = await vault.adapter.exists(`${folderPath}/${newFileName}.md`);
        counter++;
    }

    return `${folderPath}/${newFileName}`;
}

module.exports = createNote;

