import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "SL Business Intelligence Copilot",
  description: "Sri Lankan business and land intelligence",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
