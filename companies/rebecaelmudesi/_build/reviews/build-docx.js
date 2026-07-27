#!/usr/bin/env node
/* Rebeca Elmúdesi — DOCX styles base + letterhead. Charter-driven, Helvetica throughout,
   black headings, red accent, justified body, A4, hairline-rule footer. */
const fs = require('fs');
const path = require('path');
const {
  Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType,
  Header, Footer, PageNumber, TabStopType, TabStopPosition, BorderStyle,
  ImageRun, LevelFormat, convertInchesToTwip, convertMillimetersToTwip,
} = require('docx');

const BRAND = path.resolve(__dirname, '..', '..');
const charter = JSON.parse(fs.readFileSync(path.join(BRAND, 'charter.json'), 'utf8'));
const OUT = path.join(BRAND, 'templates', 'docx');
fs.mkdirSync(OUT, { recursive: true });

const C = charter.colors, F = charter.fonts;
const HEAD = F.heading.family, BODY = F.body.family, MONO = F.mono.family;
const INK = (C.text || '#000000').replace('#', '');
const ACCENT = (C.accent || '#fe0200').replace('#', '');
const GREY = (C.textLight || '#b4b4b4').replace('#', '');
const HEADCLR = (charter.document.headingColor || '#000000').replace('#', '');
const NAME = charter.meta.displayName;
const TAGLINE = charter.meta.tagline;

const A4 = { width: 11906, height: 16838 };
const M = charter.document.margins || { top: 0.71, bottom: 0.71, left: 0.71, right: 0.71 };
const margin = {
  top: convertInchesToTwip(M.top), bottom: convertInchesToTwip(M.bottom),
  left: convertInchesToTwip(M.left), right: convertInchesToTwip(M.right),
};

const headingStyle = (id, name, sizePt, lvl) => ({
  id, name, basedOn: 'Normal', next: 'Normal', quickFormat: true,
  run: { font: HEAD, size: sizePt * 2, bold: true, color: HEADCLR },
  paragraph: { outlineLevel: lvl, spacing: { before: 240, after: 120 }, alignment: AlignmentType.LEFT },
});

const styles = {
  default: { document: { run: { font: BODY, size: 22, color: INK } } },
  paragraphStyles: [
    { id: 'Normal', name: 'Normal', run: { font: BODY, size: 22, color: INK },
      paragraph: { alignment: AlignmentType.JUSTIFIED, spacing: { line: 276, after: 160 } } },
    headingStyle('Heading1', 'Heading 1', 24, 0),
    headingStyle('Heading2', 'Heading 2', 20, 1),
    headingStyle('Heading3', 'Heading 3', 16, 2),
    headingStyle('Heading4', 'Heading 4', 14, 3),
    headingStyle('Heading5', 'Heading 5', 12, 4),
    headingStyle('Heading6', 'Heading 6', 11, 5),
    { id: 'Caption', name: 'Caption', basedOn: 'Normal', next: 'Normal',
      run: { font: BODY, size: 18, italics: true, color: GREY },
      paragraph: { alignment: AlignmentType.LEFT, spacing: { after: 120 } } },
    { id: 'Quote', name: 'Quote', basedOn: 'Normal', next: 'Normal',
      run: { font: BODY, size: 22, italics: true, color: INK },
      paragraph: { indent: { left: convertInchesToTwip(0.4) }, alignment: AlignmentType.LEFT,
        border: { left: { style: BorderStyle.SINGLE, size: 18, color: ACCENT, space: 12 } } } },
  ],
  characterStyles: [
    { id: 'Hyperlink', name: 'Hyperlink', basedOn: 'DefaultParagraphFont',
      run: { color: ACCENT, underline: {} } },
  ],
};

const numbering = {
  config: [
    { reference: 'bullets', levels: [{ level: 0, format: LevelFormat.BULLET, text: '—', alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 360, hanging: 260 } } } }] },
    { reference: 'numbers', levels: [{ level: 0, format: LevelFormat.DECIMAL, text: '%1.', alignment: AlignmentType.LEFT,
      style: { paragraph: { indent: { left: 360, hanging: 260 } } } }] },
  ],
};

function footer(extra) {
  return new Footer({ children: [
    new Paragraph({ border: { top: { style: BorderStyle.SINGLE, size: 6, color: INK, space: 6 } },
      tabStops: [{ type: TabStopType.RIGHT, position: TabStopPosition.MAX }],
      children: [
        new TextRun({ text: extra || NAME, font: BODY, size: 16, color: GREY }),
        new TextRun({ text: '\t', font: BODY, size: 16 }),
        new TextRun({ children: ['', PageNumber.CURRENT], font: MONO, size: 16, color: GREY }),
      ] }),
  ] });
}

// ---------- styles.docx (empty body, full styles) ----------
async function buildStyles() {
  const logoPng = fs.readFileSync(path.join(BRAND, 'logos', 'wordmark.png'));
  const doc = new Document({
    styles, numbering, features: { updateFields: true },
    sections: [{
      properties: { page: { size: { width: A4.width, height: A4.height }, margin } },
      headers: { default: new Header({ children: [
        new Paragraph({ alignment: AlignmentType.RIGHT, children: [
          new TextRun({ text: NAME.toUpperCase(), font: HEAD, size: 16, color: GREY, characterSpacing: 40 }) ] }) ] }) },
      footers: { default: footer() },
      children: [ new Paragraph({ children: [
        new ImageRun({ data: logoPng, transformation: { width: 150, height: 32 } }) ] }), new Paragraph({ text: '' }) ],
    }],
  });
  fs.writeFileSync(path.join(OUT, 'styles.docx'), await Packer.toBuffer(doc));
  console.log('wrote templates/docx/styles.docx');
}

// ---------- letterhead.docx ----------
async function buildLetterhead() {
  const accentRule = (color, indent) => new Paragraph({
    indent: indent ? { left: convertInchesToTwip(indent) } : undefined,
    border: { bottom: { style: BorderStyle.SINGLE, size: 10, color, space: 1 } },
    spacing: { after: indent ? 200 : 20 }, children: [new TextRun({ text: '', size: 2 })],
  });
  const firstHeader = new Header({ children: [
    new Paragraph({ spacing: { after: 40 }, children: [
      new TextRun({ text: NAME, font: HEAD, size: 28, bold: true, characterSpacing: 20, color: INK }) ] }),
    new Paragraph({ spacing: { after: 120 }, children: [
      new TextRun({ text: TAGLINE, font: BODY, size: 18, italics: true, color: GREY }) ] }),
    accentRule(INK, 0), accentRule(ACCENT, 0.25),
  ] });
  const contHeader = new Header({ children: [
    new Paragraph({ children: [
      new TextRun({ text: NAME.toUpperCase(), font: HEAD, size: 16, characterSpacing: 40, color: GREY }),
      new TextRun({ text: '  .', font: HEAD, size: 16, bold: true, color: ACCENT }) ] }) ] });

  const doc = new Document({
    styles, numbering,
    sections: [{
      properties: {
        titlePage: true,
        page: { size: { width: A4.width, height: A4.height },
          margin: { ...margin, top: convertInchesToTwip(1.8) } },
      },
      headers: { first: firstHeader, default: contHeader },
      footers: {
        first: footer('rebeca.elmudesi@gmail.com   ·   @elmudesi.studio'),
        default: footer('rebeca.elmudesi@gmail.com   ·   @elmudesi.studio'),
      },
      children: [
        new Paragraph({ alignment: AlignmentType.RIGHT, spacing: { after: 240 },
          children: [new TextRun({ text: '[Date]', font: MONO, size: 18, color: GREY })] }),
        new Paragraph({ children: [new TextRun({ text: '[Recipient name]', bold: true })] }),
        new Paragraph({ style: 'Caption', children: [new TextRun({ text: '[Gallery / address]', italics: true })] }),
        new Paragraph({ spacing: { before: 160, after: 160 }, children: [
          new TextRun({ text: 'Re: ', bold: true, color: ACCENT }),
          new TextRun({ text: '[Subject]' }) ] }),
        new Paragraph({ children: [new TextRun({ text: 'Dear [Name],' })] }),
        new Paragraph({ children: [new TextRun({ text: '[Body — replace this paragraph. Body text is justified, Helvetica, with the brand hairline footer below. Keep it spare.]', color: GREY })] }),
        new Paragraph({ spacing: { before: 320 }, children: [new TextRun({ text: 'With kind regards,' })] }),
        new Paragraph({ spacing: { before: 360 }, children: [new TextRun({ text: NAME, bold: true })] }),
        new Paragraph({ style: 'Caption', children: [new TextRun({ text: TAGLINE, italics: true })] }),
      ],
    }],
  });
  fs.writeFileSync(path.join(OUT, 'letterhead.docx'), await Packer.toBuffer(doc));
  console.log('wrote templates/docx/letterhead.docx');
}

(async () => { await buildStyles(); await buildLetterhead(); })();
