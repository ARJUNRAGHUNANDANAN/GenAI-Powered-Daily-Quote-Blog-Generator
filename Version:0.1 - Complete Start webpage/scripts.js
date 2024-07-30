document.addEventListener('DOMContentLoaded', function() {
    const postsContainer = document.getElementById('posts-container');
    const postsDirectory = '_posts/';
    const postIndexFile = '_posts/post_index.json';

    fetch(postIndexFile)
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(postIndex => {
            console.log('Fetched post index:', postIndex);
            Object.entries(postIndex).forEach(([mdFile, imgFile]) => {
                fetchMarkdownFile(postsDirectory + mdFile, imgFile);
            });
        })
        .catch(error => {
            console.error('Error fetching post index:', error);
        });

    function fetchMarkdownFile(file, image) {
        fetch(file)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.text();
            })
            .then(data => {
                console.log('Fetched markdown file:', file);
                const metadata = parseMetadata(data);
                if (metadata) {
                    createPostCard(metadata, image, file);
                }
            })
            .catch(error => {
                console.error('Error fetching markdown file:', error);
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

    function createPostCard(metadata, image, file) {
        const postCard = document.createElement('div');
        postCard.className = 'col-md-4';

        postCard.innerHTML = `
            <a href="post.html?md=${encodeURIComponent(file)}&img=${encodeURIComponent(image)}" class="card-link">
                <div class="card">
                    <img src="${postsDirectory + image}" class="card-img-top" alt="${metadata.title}">
                    <div class="card-body">
                        <h5 class="card-title">${metadata.title}</h5>
                        <p class="card-text">${metadata.excerpt}</p>
                    </div>
                </div>
            </a>
        `;

        postsContainer.appendChild(postCard);
    }
});
