// Obsidian Templater template for insert link to file from clipboard
// 1. Check clipboard and return markdown with text of file path and link to file (file:///...)
// 2. File or folder can not be exists, so no need to check it.
// 3. Path can be in such forms:
// a) C:/tmp 
// b) C:\tmp 
// c) file:///tmp
// Need to process any format, but text of markdown title must be with usual slashes, and link in format with usual slashes (C:/tmp)
// 4. Spaces and other strange symbols in file name must be encoded
async function insertFileLink(tp) {
  try {
    const clipboardContent = await tp.system.clipboard();
    const result = await getClipboardContent(clipboardContent);
    return `[${result.title}](${result.link})`;
  }
  catch (e) {
    console.error(e);
    return {text: e.stack};
  }
}

// This function must return {title: title, link: file:///...}
async function getClipboardContent(clipboardContent) {

  const formattedPath = clipboardContent
    .replace(/\\/g, '/') // Convert backslashes to forward slashes
    .replace(/^file:\/\//, ''); // Remove 'file://' if present

  // Adjusted title logic to remove leading slash if present
  const title = decodeURIComponent(formattedPath.startsWith('/') ? formattedPath.slice(1) : formattedPath); // Decode URL-encoded characters
  const link = formattedPath.startsWith('/') ? formattedPath.slice(1) : formattedPath; // Remove leading slash if present

  console.log("Title:", title); // Log the title to console
  // Update the link formatting to avoid extra slashes
  console.log("Link:", link); // Log the link to console

  return { title: title, link: link }; // Change 'text' to 'title'
}

module.exports = insertFileLink;

// todo: write main test function for getClipboardContent for each case
// format: {title: title, link: link}
//
// examples: 
//C:\Users\User\Documents\Obsidian\
//[C:/Users/User/Documents/Obsidian/](C:/Users/User/Documents/Obsidian/)
//
//C:/Users/User/Documents/Obsidian/Home/Home/Misc/Templater/Scripts/
//[C:/Users/User/Documents/Obsidian/Home/Home/Misc/Templater/Scripts/](C:/Users/User/Documents/Obsidian/Home/Home/Misc/Templater/Scripts/)
//
//file:///C:/Users/User/Games/Age%20of%20Empires%202%20DE
//[C:/Users/User/Games/Age of Empires 2 DE](C:/Users/User/Games/Age%20of%20Empires%202%20DE)

async function test() {
  const testCases = [
    {
      clipboardContent: 'C:\\Users\\User\\Documents\\Obsidian\\',
      expected: {title: 'C:/Users/User/Documents/Obsidian/', link: 'C:/Users/User/Documents/Obsidian/'}
    },
    {
      clipboardContent: 'C:/Users/User/Documents/Obsidian/Home/Home/Misc/Templater/Scripts/',
      expected: {title: 'C:/Users/User/Documents/Obsidian/Home/Home/Misc/Templater/Scripts/', link: 'C:/Users/User/Documents/Obsidian/Home/Home/Misc/Templater/Scripts/'}
    },
    {
      clipboardContent: 'file:///C:/Users/User/Games/Age%20of%20Empires%202%20DE',
      expected: {title: 'C:/Users/User/Games/Age of Empires 2 DE', link: 'C:/Users/User/Games/Age%20of%20Empires%202%20DE'}
    }
  ];

  for (const testCase of testCases) {
    const result = await getClipboardContent(testCase.clipboardContent);
    console.log("----------------------------------------");
    console.log("Clipboard Content:", testCase.clipboardContent);
    console.log("Expected Result:", testCase.expected);
    console.log("Test Result:", result); // Log the result
    console.log("--- JSON ---");
    const resultString = JSON.stringify(result);
    const expectedString = JSON.stringify(testCase.expected);
    console.log("Result String:", resultString);
    console.log("Expected String:", expectedString);
    console.log("Test Result Matches Expected:", resultString === expectedString);
    console.log("----------------------------------------");
  }
}

test();








