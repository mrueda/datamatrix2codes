import Link from '@docusaurus/Link';
import Layout from '@theme/Layout';
import styles from './index.module.css';

const links = [
  {
    label: 'macOS Excel',
    title: 'Install the VBA module on Mac',
    text: 'Import the macro, save an .xlsm workbook, and run the setup macro for scanner columns.',
    to: '/docs/installation/macos',
  },
  {
    label: 'Windows Excel',
    title: 'Install the VBA module on Windows',
    text: 'Enable trusted macros, import the module, and use the same worksheet feedback colors.',
    to: '/docs/installation/windows',
  },
  {
    label: 'Review',
    title: 'Understand status colors',
    text: 'Use OK, PARTIAL, AMBIGUOUS, and UNPARSED feedback to decide what needs pharmacist review.',
    to: '/docs/usage/excel-feedback',
  },
  {
    label: 'Reference',
    title: 'Batch-check with Python',
    text: 'Run the reference parser outside Excel to validate fixtures and scanner output on any platform.',
    to: '/docs/usage/python-cli',
  },
];

export default function Home() {
  return (
    <Layout
      title="datamatrix2codes"
      description="GS1 DataMatrix parsing for pharmacy scanner-to-Excel workflows">
      <main className={styles.page}>
        <section className={styles.hero}>
          <div className={styles.heroInner}>
            <div className={styles.copy}>
              <p className={styles.kicker}>Pharmacy scanner to Excel</p>
              <h1>Decode flattened GS1 DataMatrix strings without hiding uncertainty.</h1>
              <p className={styles.lede}>
                Built for real third-party scanners that type one raw string into Excel.
                The VBA module extracts PC, SN, LOTE, and CAD, then colors rows so
                pharmacists can review only the scans that need attention.
              </p>
              <div className={styles.actions}>
                <Link className="button button--primary button--lg" to="/docs/usage/excel-quickstart">
                  Excel quick start
                </Link>
                <Link className="button button--secondary button--lg" to="/docs/overview">
                  Read the docs
                </Link>
              </div>
            </div>

            <div className={styles.sheetPreview} aria-label="Synthetic Excel feedback preview">
              <div className={styles.sheetTitle}>Scanner review</div>
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
