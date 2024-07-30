document.addEventListener('DOMContentLoaded', function() {
    const params = new URLSearchParams(window.location.search);
    const mdFile = params.get('md');
    const imgFile = params.get('img');

    if (mdFile && imgFile) {
        fetchMarkdownContent(mdFile, imgFile);
    } else {
        document.getElementById('post-content').innerHTML = '<p>Error loading post content.</p>';
    }

    function fetchMarkdownContent(mdFile, imgFile) {
        fetch(mdFile)
            .then(response => response.text())
            .then(markdown => {
                const postContent = document.getElementById('post-content');
                const metadata = parseMetadata(markdown);

                if (metadata) {
                    postContent.innerHTML = `
                        <div class="text-center mb-4">
                            <img src="_posts/${imgFile}" class="img-fluid" alt="${metadata.title}">
                        </div>
                        <h1>${metadata.title}</h1>
                        <div id="post-body"></div>
                    `;
                    renderMarkdown(markdown);
                } else {
                    postContent.innerHTML = '<p>Error loading post content.</p>';
                }
            })
            .catch(error => {
                console.error('Error fetching markdown file:', error);
                document.getElementById('post-content').innerHTML = '<p>Error loading post content.</p>';
            });
    }

    function parseMetadata(markdown) {
        const metadataRegex = /---\n([\s\S]+?)\n---/;
        const match = markdown.match(metadataRegex);
        if (match) {
            const metadata = match[1].split('\n').reduce((acc, line) => {
                const [key, value] = line.split(': ');
                acc[key.trim()] = value.trim().replace(/"/g, '');
                return acc;
            }, {});
            return metadata;
        }
        return null;
    }

    function renderMarkdown(markdown) {
        const content = markdown.replace(/---\n[\s\S]+?\n---/, ''); // Remove the metadata block
        document.getElementById('post-body').innerHTML = marked(content);
    }
});
