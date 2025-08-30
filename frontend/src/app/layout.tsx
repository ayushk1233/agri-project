import './global.css';

export const metadata = {
  title: 'AgriProject Chat',
  description: 'A chat application for agricultural assistance',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}