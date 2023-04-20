import { BackButton } from "../components/Buttons";

function NotFound() {
  return (
    <>
      <BackButton/>
      <div className="content">
        <h2 className="error">
          404: Page not found.
        </h2>
      </div>
    </>
  );
}

export default NotFound;