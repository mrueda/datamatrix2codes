import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: 'datamatrix2codes Docs',
  tagline: 'GS1 DataMatrix parsing for pharmacy scanner-to-Excel workflows',
  url: 'https://mrueda.github.io',
  baseUrl: '/datamatrix2codes/',
  organizationName: 'mrueda',
  projectName: 'datamatrix2codes',
  onBrokenLinks: 'warn',
  markdown: {
    hooks: {
      onBrokenMarkdownLinks: 'warn',
    },
  },
  i18n: {
    defaultLocale: 'en',
    locales: ['en'],
  },
  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          routeBasePath: 'docs',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],
  themes: [
    [
      '@easyops-cn/docusaurus-search-local',
      {
        hashed: true,
        language: ['en'],
        indexDocs: true,
        indexBlog: false,
        docsRouteBasePath: '/docs',
      },
    ],
  ],
  themeConfig: {
    image: 'img/excel-status-feedback.png',
    colorMode: {
      respectPrefersColorScheme: true,
    },
    navbar: {
      title: 'datamatrix2codes',
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'docsSidebar',
          position: 'left',
          label: 'Docs',
        },
        {
          to: '/docs/installation/macos',
          label: 'macOS',
          position: 'left',
        },
        {
          to: '/docs/installation/windows',
          label: 'Windows',
          position: 'left',
        },
        {
          href: 'https://raw.githubusercontent.com/mrueda/datamatrix2codes/master/macro/ParseEncodedString.bas',
          label: 'Download BAS',
          position: 'right',
        },
        {
          href: 'https://github.com/mrueda/datamatrix2codes',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: 'Docs',
          items: [
            {label: 'Overview', to: '/docs/overview'},
            {label: 'Excel Quick Start', to: '/docs/usage/excel-quickstart'},
            {label: 'macOS Install', to: '/docs/installation/macos'},
            {label: 'Windows Install', to: '/docs/installation/windows'},
            {label: 'Troubleshooting', to: '/docs/usage/troubleshooting'},
          ],
        },
        {
          title: 'Project',
          items: [
            {label: 'Repository', href: 'https://github.com/mrueda/datamatrix2codes'},
            {label: 'License', href: 'https://github.com/mrueda/datamatrix2codes/blob/main/LICENSE'},
          ],
        },
      ],
      copyright: 'Copyright (C) 2026 Manuel Rueda.',
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
