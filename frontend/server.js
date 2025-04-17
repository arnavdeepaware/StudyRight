import express from 'express';
import path from 'path';
import { promises as fs } from 'fs';
import { fileURLToPath } from 'url';
import cors from 'cors';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
const PORT = 3001;

app.use(cors());

app.get('/prev-videos', async (req, res) => {
  try {
    const videosPath = path.join(__dirname, 'public', 'prev-videos');
    const files = await fs.readdir(videosPath);
    
    // Get file stats and create detailed response
    const videoFiles = await Promise.all(
      files
        .filter(file => file.endsWith('.mp4'))
        .map(async (file) => {
          const stats = await fs.stat(path.join(videosPath, file));
          return {
            filename: file,
            url: `/prev-videos/${file}`,
            createdAt: stats.birthtime,
            size: stats.size
          };
        })
    );

    res.json({ videos: videoFiles });
  } catch (error) {
    console.error('Error reading video directory:', error);
    res.status(500).json({ error: 'Failed to read video directory' });
  }
});

app.use('/prev-videos', express.static(path.join(__dirname, 'public', 'prev-videos')));

app.listen(PORT, () => {
  console.log(`Video server running on http://localhost:${PORT}`);
});