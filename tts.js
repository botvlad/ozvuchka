import textToSpeech from "@google-cloud/text-to-speech";

const client = new textToSpeech.TextToSpeechClient({
  credentials: JSON.parse(process.env.GOOGLE_CREDENTIALS)
});

export default async function handler(req, res) {
  if (req.method !== "POST") {
    return res.status(405).end();
  }

  const { text, voice } = req.body;

  const request = {
    input: { text },
    voice: { languageCode: "es-ES", name: voice },
    audioConfig: { audioEncoding: "MP3" }
  };

  const [response] = await client.synthesizeSpeech(request);

  res.setHeader("Content-Type", "audio/mpeg");
  res.send(Buffer.from(response.audioContent, "base64"));
}
