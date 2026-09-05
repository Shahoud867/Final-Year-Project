export function LiveDemo() {
  return (
    <div style={{ height: "100vh", width: "100%" }}>
      <iframe
        src="/onclick-demo/index.html"
        title="Granite — live one-click diagnosis demo"
        style={{ width: "100%", height: "100%", border: "none", display: "block" }}
      />
    </div>
  );
}
