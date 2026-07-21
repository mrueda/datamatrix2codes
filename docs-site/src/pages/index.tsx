import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import useBaseUrl from '@docusaurus/useBaseUrl';
import styles from './index.module.css';

const links = [
  {
    label: 'Start here',
    title: 'Use it in Excel',
    text: 'Download one .bas file, import it into your workbook, scan medicine boxes, and run DataMatrix2Codes.',
    to: '/docs/usage/excel-quickstart',
  },
  {
    label: 'Download',
    title: 'Get the Excel macro',
    text: 'Excel users only need ParseEncodedString.bas. The full repository is mainly for developers and tests.',
    to: 'https://raw.githubusercontent.com/mrueda/datamatrix2codes/master/macro/ParseEncodedString.bas',
  },
  {
    label: 'Review',
    title: 'Know which rows need checking',
    text: 'Green rows are ready. Amber, orange, or gray rows need the pharmacist to check the box or scanner input.',
    to: '/docs/usage/review-colors',
  },
  {
    label: 'Install',
    title: 'Import into Excel',
    text: 'Step-by-step instructions for Excel on macOS and Windows.',
    to: '/docs/installation/macos',
  },
];

export default function Home() {
  const workflowImage = useBaseUrl('/img/excel-conversion-workflow.png');
  const logoImage = useBaseUrl('/img/logo.svg');

  return (
    <Layout
      title="datamatrix2codes"
      description="GS1 DataMatrix parsing for pharmacy scanner-to-Excel workflows">
      <main className={styles.page}>
        <section className={styles.hero}>
          <div className={styles.heroInner}>
            <div className={styles.copy}>
              <img className={styles.heroLogo} src={logoImage} alt="datamatrix2codes logo" />
              <p className={styles.kicker}>For pharmacy scanner workflows in Excel</p>
              <h1>Turn Spanish medicine box scans into PC, CAD, SN, and LOTE columns.</h1>
              <p className={styles.lede}>
                Download one Excel macro file, import it into a workbook, and scan medicine
                boxes into column A. The macro fills the pharmacy fields and colors rows so
                pharmacists know which scans are ready and which need checking.
              </p>
              <div className={styles.actions}>
                <Link className="button button--primary button--lg" to="/docs/usage/excel-quickstart">
                  Use it in Excel
                </Link>
                <Link
                  className="button button--secondary button--lg"
                  to="https://raw.githubusercontent.com/mrueda/datamatrix2codes/master/macro/ParseEncodedString.bas">
                  Download BAS file
                </Link>
              </div>
            </div>

            <div className={styles.sheetPreview} aria-label="Synthetic Excel review colors preview">
              <div className={styles.sheetTitle}>Medicine scan review in Excel</div>
              <table>
                <thead>
                  <tr>
                    <th>CODE</th>
                    <th>PC</th>
                    <th>LOTE</th>
                    <th>STATUS</th>
                  </tr>
                </thead>
                <tbody>
                  <tr className={styles.ok}>
                    <td>010843...</td>
                    <td>8435232347418</td>
                    <td>AD801</td>
                    <td>OK</td>
                  </tr>
                  <tr className={styles.partial}>
                    <td>010847...</td>
                    <td>8470006547663</td>
                    <td></td>
                    <td>PARTIAL</td>
                  </tr>
                  <tr className={styles.ambiguous}>
                    <td>010847...</td>
                    <td>8470007006817</td>
                    <td>V06</td>
                    <td>AMBIGUOUS</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <section className={styles.workflow}>
          <div className={styles.workflowInner}>
            <img
              src={workflowImage}
              alt="Synthetic Excel workbook showing raw scanner strings converted into PC, SN, LOTE, CAD, STATUS, CONFIDENCE, and EXPLAIN columns"
            />
            <p>Raw scanner strings in Excel become parsed pharmacy columns with review colors.</p>
          </div>
        </section>

        <section className={styles.sections}>
          <div className={styles.grid}>
            {links.map((link) => (
              <Link className={styles.card} to={link.to} key={link.title}>
                <span>{link.label}</span>
                <h2>{link.title}</h2>
                <p>{link.text}</p>
              </Link>
            ))}
          </div>
        </section>
      </main>
    </Layout>
  );
}
