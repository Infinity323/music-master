import { HomeButton } from "../components/Buttons";

function NotFound() {
  return (
    <>
      <HomeButton/>
      <div className="content">
        <h2 className="error">
          404: Page not found.
        </h2>
      </div>
    </>
  );
}

export default NotFound;